from django import forms
from car_service.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['firstName', 'lastName', 'idPosition', 'phoneNumber', 'email', 'idServiceCenter']
