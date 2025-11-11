from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from car_service.repositories.RepositoryManager import RepositoryManager
from .serializer import *

rm = RepositoryManager()


class BaseViewSet(viewsets.ViewSet):
    serializer_class = None
    repo = None
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = self.repo.get_all()
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

    @action(detail=False, methods=['get'])
    def report(self, request):
        repairs = self.repo.get_all()
        total_repairs = len(repairs)
        total_services = sum(
            sum(detail.idService.baseCost * detail.count for detail in r.repairdetail_set.all() if detail.idService)
            for r in repairs
        )
        total_part = sum(
            sum(detail.idPart.cost * detail.count for detail in r.repairdetail_set.all() if detail.idPart)
            for r in repairs
        )
        total_additional = sum(
            sum(rd.additionalCost for rd in r.repairdetail_set.all())
            for r in repairs
        )
        grand_total = total_services + total_part + total_additional
        return Response({
            "total_repairs": total_repairs,
            "total_service": total_services,
            "total_part": total_part,
            "total_additional": total_additional,
            "grand_total": grand_total
        })


class RepairDetailViewSet(BaseViewSet):
    serializer_class = RepairDetailSerializer
    repo = rm.repairDetail
