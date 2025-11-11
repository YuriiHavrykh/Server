from rest_framework import serializers
from car_service.models import (
    Position, ServiceCenter, Employee, Client, Car, Part, Service, Repair, RepairDetail
)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ServiceCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCenter
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class RepairSerialize(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'


class RepairDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairDetail
        fields = '__all__'
