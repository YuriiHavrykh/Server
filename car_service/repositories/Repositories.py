from car_service.models import Position
from car_service.models import ServiceCenter
from car_service.models import Employee
from car_service.models import Client
from car_service.models import Car
from car_service.models import Part
from car_service.models import Service
from car_service.models import Repair
from car_service.models import RepairDetail

from car_service.repositories.BaseRepository import BaseRepository

from django.db.models.functions import TruncMonth
from django.db.models import Count, Avg
from django.db.models import Sum, F


class PositionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Position)


class ServiceCenterRepository(BaseRepository):
    def __init__(self):
        super().__init__(ServiceCenter)


class EmployeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Employee)


class ClientRepository(BaseRepository):
    def __init__(self):
        super().__init__(Client)


class CarRepository(BaseRepository):
    def __init__(self):
        super().__init__(Car)


class PartRepository(BaseRepository):
    def __init__(self):
        super().__init__(Part)


class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Service)


class RepairRepository(BaseRepository):
    def __init__(self):
        super().__init__(Repair)

    def repairs_count_by_service_center(self):
        return (
            self.model.objects
            .values('idServiceCenter__name')
            .annotate(total_repairs=Count('idRepair'))
            .order_by('-total_repairs')
        )

    def avg_parts_per_repair_by_center(self):
        return (
            self.model.objects
            .values('idServiceCenter__name')
            .annotate(
                avg_parts=Avg(F('repairdetail__count'))

            )
            .order_by('-avg_parts')
        )

    def repairs_by_month(self):
        return (
            self.model.objects
            .annotate(month=TruncMonth('acceptenceDate'))
            .values('month')
            .annotate(total_repairs=Count('idRepair'))
            .order_by('month')
        )

    def top_clients(self, service_center_id=None):
        qs = self.model.objects

        if service_center_id is not None:
            qs = qs.filter(idServiceCenter_id=service_center_id)

        return (
            qs
            .values('idClient__firstName', 'idClient__lastName', 'idServiceCenter__name')
            .annotate(total_repairs=Count('idRepair'))
            .order_by('-total_repairs')
        )


class RepairDetailRepository(BaseRepository):
    def __init__(self):
        super().__init__(RepairDetail)

    def service_income(self):
        return (
            self.model.objects
            .filter(idService__isnull=False)
            .values('idService__serviceName')
            .annotate(
                total_income=Sum(
                    F('idService__baseCost') * F('count')
                )
            )
            .order_by('-total_income')
        )

    def part_income_with_having(self):
        return (
            self.model.objects
            .filter(idPart__isnull=False)
            .values('idPart__partName')
            .annotate(
                total_income=Sum(F('idPart__cost') * F('count'))
            )
            .filter(total_income__gt=1000)
            .order_by('-total_income')
        )
