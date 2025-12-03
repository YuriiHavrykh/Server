from django.shortcuts import render, get_object_or_404, redirect
from car_service.models import Employee
from .forms import EmployeeForm

from car_service.NetworkHelper import NetworkHelper

API_USERNAME = "admin"
API_PASSWORD = "1111"
API_URL = "http://localhost:8081/api"

helper = NetworkHelper(API_URL, API_USERNAME, API_PASSWORD)


def teams_list(request):
    if request.method == "POST":
        team_id = request.POST.get("delete_team_id")
        if team_id:
            try:
                helper.delete_team(team_id)
            except Exception as e:
                print("Error deleting team:", e)
        return redirect("teams_list")

    teams = helper.get_teams()
    return render(request, "teams_list.html", {"teams": teams})


def drivers_list(request):
    if request.method == "POST":
        driver_id = request.POST.get("delete_driver_id")
        if driver_id:
            try:
                helper.delete_driver(driver_id)
            except Exception as e:
                print("Error deleting driver:", e)
        return redirect("drivers_list")

    drivers = helper.get_drivers()
    return render(request, "drivers_list.html", {"drivers": drivers})


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee/list.html', {'employees': employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/detail.html', {'employee': employee})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee/form.html', {'form': form, 'title': "Create Employee"})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee/form.html', {'form': form, 'title': "Edit Employee"})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')

    return render(request, 'employee/delete.html', {'employee': employee})
