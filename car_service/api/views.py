from django.db.models import Count, Sum, F, Func
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import pandas as pd

from car_service.repositories.RepositoryManager import RepositoryManager
from .serializer import *
from car_service.models import Repair, RepairDetail

rm = RepositoryManager()


class BaseViewSet(viewsets.GenericViewSet):
    serializer_class = None
    repo = None
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        items = self.repo.get_all()[:1000]
        ser = self.serializer_class(items, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk=None):
        item = self.repo.get_by_id(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(item)
        return Response(ser.data)

    def create(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            obj = self.repo.create(**ser.validated_data)
            return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item = self.repo.get_by_id(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(item, data=request.data, partial=True)
        if ser.is_valid():
            obj = self.repo.update(pk, **ser.validated_data)
            return Response(self.serializer_class(obj).data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        deleted = self.repo.delete(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class PositionViewSet(BaseViewSet):
    serializer_class = PositionSerializer
    repo = rm.position


class ServiceCenterViewSet(BaseViewSet):
    serializer_class = ServiceCenterSerializer
    repo = rm.serviceCenter


class EmployeeViewSet(BaseViewSet):
    serializer_class = EmployeeSerializer
    repo = rm.employee


class ClientViewSet(BaseViewSet):
    serializer_class = ClientSerializer
    repo = rm.client


class CarViewSet(BaseViewSet):
    serializer_class = CarSerializer
    repo = rm.car


class PartViewSet(BaseViewSet):
    serializer_class = PartSerializer
    repo = rm.part


class ServiceViewSet(BaseViewSet):
    serializer_class = ServiceSerializer
    repo = rm.service


class RepairViewSet(BaseViewSet):
    serializer_class = RepairSerialize
    repo = rm.repair

    def get_queryset(self):
        return Repair.objects.none()

    @action(detail=False, methods=['get'], url_path='analytics/repairs-by-center')
    def repairs_by_center_df(self, request):
        min_repairs = request.query_params.get('min_repairs', 1)
        qs = self.repo.repairs_count_by_service_center()

        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)

        try:
            min_repairs = int(min_repairs)
            df = df[df['total_repairs'] >= min_repairs]
        except ValueError:
            pass

        df.columns = ['ServiceCenter', 'TotalRepairs']
        stats = {"mean": df['TotalRepairs'].mean(), "median": df['TotalRepairs'].median(),
                 "min": df['TotalRepairs'].min(), "max": df['TotalRepairs'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})

    @action(detail=False, methods=['get'], url_path='analytics/avg-parts-per-center')
    def avg_parts_per_repair_by_center_df(self, request):
        qs = self.repo.avg_parts_per_repair_by_center()
        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)
        df.columns = ['ServiceCenter', 'AvgParts']
        stats = {"mean": df['AvgParts'].mean(), "median": df['AvgParts'].median(), "min": df['AvgParts'].min(),
                 "max": df['AvgParts'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})

    @action(detail=False, methods=['get'], url_path='analytics/repairs-by-month')
    def repairs_by_month_df(self, request):
        qs = self.repo.repairs_by_month()
        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)

        df['month'] = pd.to_datetime(df['month'])
        df['month'] = df['month'].dt.strftime('%Y-%m')

        df.columns = ['Month', 'TotalRepairs']
        stats = {"mean": df['TotalRepairs'].mean(), "median": df['TotalRepairs'].median(),
                 "min": df['TotalRepairs'].min(), "max": df['TotalRepairs'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})

    @action(detail=False, methods=['get'], url_path='analytics/top-clients')
    def top_clients_df(self, request):

        center_id = request.query_params.get('center_id')
        qs = self.repo.top_clients(service_center_id=center_id)
        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)
        df['Client'] = df['idClient__firstName'] + ' ' + df['idClient__lastName']

        if center_id is None:
            df['Client'] = df['Client'] + ' (' + df['idServiceCenter__name'] + ')'

        df = df[['Client', 'total_repairs']]
        df.columns = ['Client', 'TotalRepairs']

        stats = {"mean": df['TotalRepairs'].mean(), "median": df['TotalRepairs'].median(),
                 "min": df['TotalRepairs'].min(), "max": df['TotalRepairs'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})

    @action(detail=False, methods=['get'], url_path='analytics/report')
    def report(self, request):
        repairs = Repair.objects.prefetch_related('repairdetail_set__idService', 'repairdetail_set__idPart')
        total_repairs = repairs.count()

        total_services = sum(
            sum(d.idService.baseCost * d.count for d in r.repairdetail_set.all() if d.idService)
            for r in repairs
        )
        total_parts = sum(
            sum(d.idPart.cost * d.count for d in r.repairdetail_set.all() if d.idPart)
            for r in repairs
        )
        total_additional = sum(
            sum(d.additionalCost for d in r.repairdetail_set.all())
            for r in repairs
        )
        grand_total = total_services + total_parts + total_additional

        return Response({
            "total_repairs": total_repairs,
            "total_services": total_services,
            "total_parts": total_parts,
            "total_additional": total_additional,
            "grand_total": grand_total
        })


class RepairDetailViewSet(BaseViewSet):
    serializer_class = RepairDetailSerializer
    repo = rm.repairDetail

    def get_queryset(self):
        return RepairDetail.objects.none()

    @action(detail=False, methods=['get'], url_path='analytics/service-income')
    def service_income_df(self, request):
        qs = self.repo.service_income()
        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)
        df.columns = ['ServiceName', 'TotalIncome']
        stats = {"mean": df['TotalIncome'].mean(), "median": df['TotalIncome'].median(), "min": df['TotalIncome'].min(),
                 "max": df['TotalIncome'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})

    @action(detail=False, methods=['get'], url_path='analytics/part-income-having')
    def part_income_df(self, request):
        qs = self.repo.part_income()
        df = pd.DataFrame(list(qs))
        if df.empty: return Response({"data": [], "stats": {}}, status=status.HTTP_204_NO_CONTENT)
        df.columns = ['PartName', 'TotalIncome']
        stats = {"mean": df['TotalIncome'].mean(), "median": df['TotalIncome'].median(), "min": df['TotalIncome'].min(),
                 "max": df['TotalIncome'].max()}
        return Response({"data": df.to_dict(orient='records'), "stats": stats})
