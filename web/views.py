from django.shortcuts import render, get_object_or_404, redirect
from car_service.models import Employee, ServiceCenter
from web.dashboard_utils import fetch_data, get_plot_html
from bokeh.resources import CDN
from bokeh.embed import server_document
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


API_ENDPOINTS = {
    1: 'repairs/analytics/repairs-by-center',
    2: 'repairs/analytics/avg-parts-per-center',
    3: 'repairs/analytics/repairs-by-month',
    4: 'repairs/analytics/top-clients',  # Тут буде фільтр center_id
    5: 'repair-details/analytics/service-income',
    6: 'repair-details/analytics/part-income-having',
}


def get_service_centers():
    return ServiceCenter.objects.all()


def get_all_plots_context(framework, request_params={}):
    context = {}

    center_id = request_params.get('center_id')
    min_repairs = request_params.get('min_repairs')

    for i in range(1, 7):
        endpoint = API_ENDPOINTS[i]
        params = {}
        title_suffix = ""

        if i == 1 and min_repairs:
            params['min_repairs'] = min_repairs

        if i == 4 and center_id:
            params['center_id'] = center_id
            try:
                center = ServiceCenter.objects.get(idServiceCenter=center_id)
                title_suffix = f" (Центр: {center.name})"
            except ServiceCenter.DoesNotExist:
                pass

        df = fetch_data(endpoint, params=params)
        plot_html = get_plot_html(i, framework, df, title_suffix=title_suffix)
        context[f'plot_{i}'] = plot_html

    context['service_centers'] = get_service_centers()
    context['selected_center_id'] = int(center_id) if center_id else None

    context['min_repairs'] = int(min_repairs) if min_repairs and min_repairs.isdigit() else 100000

    return context


def dashboard_v1_plotly(request):
    context = get_all_plots_context('plotly', request_params=request.GET)
    return render(request, 'web/dashboards/dashboard.html', context)


def dashboard_v2_bokeh(request):
    context = get_all_plots_context('bokeh', request_params=request.GET)
    context['bokeh_resources'] = CDN.render()
    context['title'] = "Dashboard (Bokeh)"
    return render(request, 'web/dashboards/dashboard.html', context)
