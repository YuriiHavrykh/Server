import plotly.express as px
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.transform import cumsum
import pandas as pd
import requests
from math import pi

API_BASE_URL = "http://127.0.0.1:8000/api/"


def fetch_data(endpoint, params={}):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get('data', [])
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        return pd.DataFrame()


def plot_1_repairs_by_center_plotly(df, title_suffix=""):
    if df.empty: return "<h2>No Data</h2>"
    fig = px.bar(df, x='ServiceCenter', y='TotalRepairs',
                 title=f'Кількість ремонтів по Сервісних Центрах {title_suffix} (Plotly)',
                 color='TotalRepairs',
                 labels={'TotalRepairs': 'Кількість ремонтів', 'ServiceCenter': 'Сервісний Центр'})
    return fig.to_html(full_html=False)


def plot_1_repairs_by_center_bokeh(df, title_suffix=""):
    if df.empty: return "<h2>No Data</h2>"
    source = ColumnDataSource(df)
    p = figure(x_range=df['ServiceCenter'], height=350,
               title=f"Кількість ремонтів по Сервісних Центрах {title_suffix} (Bokeh)",
               tools="hover", tooltips=[("Центр", "@ServiceCenter"), ("Ремонти", "@TotalRepairs")])
    p.vbar(x='ServiceCenter', top='TotalRepairs', width=0.9, source=source, color="#CAB2D6")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    script, div = components(p)
    return script + div


def plot_2_avg_parts_plotly(df):
    if df.empty: return "<h2>No Data</h2>"
    fig = px.bar(df, x='ServiceCenter', y='AvgParts',
                 title='Середня кількість деталей на ремонт по Центрах (Plotly)',
                 labels={'AvgParts': 'Середня кількість деталей', 'ServiceCenter': 'Сервісний Центр'})
    return fig.to_html(full_html=False)


def plot_2_avg_parts_bokeh(df):
    if df.empty: return "<h2>No Data</h2>"
    source = ColumnDataSource(df)
    p = figure(x_range=df['ServiceCenter'], height=350,
               title="Середня кількість деталей на ремонт по Центрах (Bokeh)", tools="")
    p.vbar(x='ServiceCenter', top='AvgParts', width=0.7, source=source, color="#FDBF6F")
    p.y_range.start = 0
    script, div = components(p)
    return script + div


def plot_3_repairs_by_month_plotly(df):
    if df.empty: return "<h2>No Data</h2>"
    df['Month'] = pd.to_datetime(df['Month'])
    df = df.sort_values(by='Month')

    fig = px.line(df, x='Month', y='TotalRepairs',
                  title='Кількість ремонтів по Місяцях (Plotly)',
                  markers=True,
                  labels={'TotalRepairs': 'Кількість ремонтів', 'Month': 'Місяць'})
    return fig.to_html(full_html=False)


def plot_3_repairs_by_month_bokeh(df):
    if df.empty: return "<h2>No Data</h2>"
    df['Month_dt'] = pd.to_datetime(df['Month'])
    df = df.sort_values(by='Month_dt')
    source = ColumnDataSource(df)

    p = figure(height=350, x_axis_type="datetime", title="Кількість ремонтів по Місяцях (Bokeh)")
    p.line(x='Month_dt', y='TotalRepairs', source=source, line_width=2, color="#B2DF8A")
    p.circle(x='Month_dt', y='TotalRepairs', source=source, size=8, color="#B2DF8A")
    script, div = components(p)
    return script + div


def plot_4_top_clients_plotly(df):
    if df.empty: return "<h2>No Data</h2>"
    df = df.nlargest(10, 'TotalRepairs')
    fig = px.bar(df, x='TotalRepairs', y='Client', orientation='h',
                 title='Топ 10 Клієнтів за кількістю ремонтів (Plotly)',
                 labels={'TotalRepairs': 'Кількість ремонтів', 'Client': 'Клієнт'})
    fig.update_layout(yaxis={'autorange': "reversed"})
    return fig.to_html(full_html=False)


def plot_4_top_clients_bokeh(df):
    if df.empty: return "<h2>No Data</h2>"
    df = df.nlargest(10, 'TotalRepairs').sort_values(by='TotalRepairs')
    source = ColumnDataSource(df)
    p = figure(y_range=df['Client'], height=350,
               title="Топ 10 Клієнтів за кількістю ремонтів (Bokeh)")
    p.hbar(y='Client', right='TotalRepairs', height=0.7, source=source, color="#33A02C")
    p.x_range.start = 0
    script, div = components(p)
    return script + div


def plot_5_service_income_plotly(df):
    if df.empty: return "<h2>No Data</h2>"
    df = df.nlargest(5, 'TotalIncome')
    fig = px.pie(df, values='TotalIncome', names='ServiceName',
                 title='Дохід по Послугах  (Plotly)',
                 hole=.3)
    return fig.to_html(full_html=False)


def plot_5_service_income_bokeh(df):
    if df.empty: return "<h2>No Data</h2>"
    df = df.nlargest(5, 'TotalIncome')
    df['angle'] = df['TotalIncome'] / df['TotalIncome'].sum() * 2 * pi
    df['color'] = px.colors.qualitative.Pastel[:len(df)]
    source = ColumnDataSource(df)

    p = figure(height=350, toolbar_location=None,
               title="Дохід по Послугах  (Bokeh)", tools="hover", tooltips="@ServiceName: @TotalIncome",
               x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='ServiceName', source=source)
    p.axis.visible = False
    p.grid.grid_line_color = None
    script, div = components(p)
    return script + div


def plot_6_part_income_plotly(df):
    if df.empty: return "<h2>No Data</h2>"
    fig = px.bar(df, x='PartName', y='TotalIncome',
                 title='Дохід по Деталях (Plotly)',
                 labels={'TotalIncome': 'Сумарний Дохід', 'PartName': 'Деталь'})
    return fig.to_html(full_html=False)


def plot_6_part_income_bokeh(df):
    if df.empty: return "<h2>No Data</h2>"
    source = ColumnDataSource(df)
    p = figure(x_range=df['PartName'], height=350,
               title="Дохід по Деталях (Bokeh)", tools="")
    p.vbar(x='PartName', top='TotalIncome', width=0.8, source=source, color="#FB9A99")
    p.y_range.start = 0
    p.yaxis.formatter = NumeralTickFormatter(format="$0.00")
    script, div = components(p)
    return script + div


def get_plot_html(plot_number, framework, df, title_suffix=""):
    plots = {
        'plotly': {1: plot_1_repairs_by_center_plotly, 2: plot_2_avg_parts_plotly, 3: plot_3_repairs_by_month_plotly,
                   4: plot_4_top_clients_plotly, 5: plot_5_service_income_plotly, 6: plot_6_part_income_plotly},
        'bokeh': {1: plot_1_repairs_by_center_bokeh, 2: plot_2_avg_parts_bokeh, 3: plot_3_repairs_by_month_bokeh,
                  4: plot_4_top_clients_bokeh, 5: plot_5_service_income_bokeh, 6: plot_6_part_income_bokeh}
    }

    plot_func = plots.get(framework, {}).get(plot_number)
    if plot_func:
        if plot_number == 1 and framework == 'plotly':
            return plot_func(df, title_suffix)
        return plot_func(df)
    return "Графік не знайдено."
