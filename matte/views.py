import json

from django.shortcuts import render
from graphos.renderers.c3js import BarChart as C3BarChart
from graphos.renderers.c3js import ColumnChart as C3ColumnChart
from graphos.renderers.c3js import LineChart as C3LineChart
from graphos.renderers.c3js import PieChart as C3PieChart
from graphos.renderers.highcharts import AreaChart as HighchartsAreaChart
from graphos.renderers.highcharts import BarChart as HighchartsBarChart
from graphos.renderers.highcharts import Bubble
from graphos.renderers.highcharts import ColumnChart as HighchartsColumnChart
from graphos.renderers.highcharts import \
    ColumnLineChart as HighChartColumnLineChart
from graphos.renderers.highcharts import DonutChart as HighchartsDonutChart
from graphos.renderers.highcharts import Funnel
from graphos.renderers.highcharts import HeatMap
from graphos.renderers.highcharts import HighMap
from graphos.renderers.highcharts import LineChart as HighchartsLineChart
from graphos.renderers.highcharts import \
    LineColumnChart as HighChartLineColumnChart
from graphos.renderers.highcharts import \
    MultiAxisChart as HighChartMultiAxisChart
from graphos.renderers.highcharts import PieChart as HighchartsPieChart
from graphos.renderers.highcharts import PieDonut
from graphos.renderers.highcharts import ScatterChart as HighchartsScatterChart
from graphos.renderers.highcharts import TreeMap
from graphos.sources.simple import SimpleDataSource
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlalchemy import create_engine

from .models import Storyboard
import matte.viz

chart_klasses = {}
chart_klasses['highcharts'] = {
    'line': HighchartsLineChart,
    'bar': HighchartsBarChart,
    'column': HighchartsColumnChart,
    'pie': HighchartsPieChart,
    'donut': HighchartsDonutChart,
    'area': HighchartsAreaChart,
    'scatter': HighchartsScatterChart,
    'dual_axis': HighChartMultiAxisChart,
    'line_column': HighChartLineColumnChart,
    'column_line': HighChartColumnLineChart,
    'map': HighMap,
    'heatmap': HeatMap,
    'funnel': Funnel,
    'treemap': TreeMap,
    'piedonut': PieDonut,
    'bubble': Bubble
}
chart_klasses['c3js'] = {
    'line': C3LineChart,
    'bar': C3BarChart,
    'column': C3ColumnChart,
    'pie': C3PieChart,
}


def index(request):
    return render(request, 'index.html')


class UrlRoute(APIView):

    def get(self, request, url, *args, **kwargs):
        storyboard = [x for x in Storyboard._all if x.url == url][0]
        data = []
        for each in storyboard.get_visualizations():
            data.append(get_chart_specific_data(each.data, each.chart_type, each.chart_kind))
        return Response(data)


def get_highcharts_data(chart_klass, data_source, options={}):
    # Clean options
    if 'colors' in options:
        options['colors'] = options['colors'].split(',')
    # Clean options
    chart = chart_klass(data_source, options=options)
    highcharts_data = {
        'data_series': chart.get_series(),
        'title': options.get('title'),
        'subtitle': options.get('subtitle'),
        'plot_options': chart.get_plot_options(),
        'y_axis': chart.get_y_axis(),
        'x_axis': chart.get_x_axis(),
        'chart': chart.get_chart(),
        'credits': chart.get_credits(),
        'legend': chart.get_legend(),
        'tooltip': chart.get_tooltip()
    }
    if highcharts_data['credits'] == {}:
        highcharts_data['credits'] = {'enabled': False}
    if chart_klass == HighMap:
        del highcharts_data['x_axis']
        del highcharts_data['y_axis']
        highcharts_data.update({'map_area': chart.get_map(), 'color_axis': chart.get_color_axis(), 'series_type': chart.series_type, 'map_type': chart.get_chart_type()})
    if chart_klass == HeatMap:
        highcharts_data.update({'color_axis': chart.get_color_axis()})
    return highcharts_data


def get_chart_klass(chart_kind, chart_type):
    return chart_klasses[chart_kind][chart_type]


def get_c3_data(chart_klass, data_source, options=None):
    chart = chart_klass(data_source, options=options)
    c3_data = {
        'title': chart.get_options().get('title'),
        'x_axis_title': chart.get_x_axis_title(),
    }
    if chart_klass is C3PieChart:
        chart_data = json.loads(chart.get_data())
    else:
        chart_data = json.loads(chart.get_columns_data())
    c3_data.update({'c3data': chart_data})
    return c3_data


def get_chart_specific_data(data, chart_type, chart_kind, options={}):
    """
    Arguments:
    data: [[]]: A list of lists. This should be in the format usable by SimpleDataSource
    chart_type: Whether we want line, or bar, or column etc.
    chart_kind: Whether highcharts or c3

    Returns:
    {}: Dictionary: Keys of returned dictionary will differ based on chart_type and chart_kind.
        For highcharts, this dictionary must contain x_axis_title, categories, data_series etc.
        For c3js, this dictionary must contain c3data, x_axis_title etc.

    This assumes that only supported chart_type and chart_kind will be passed.
    """
    if chart_type != 'table':
        data = get_formatted_data(data)
        simple_data_source = SimpleDataSource(data)
        chart_klass = get_chart_klass(chart_kind, chart_type)
        if chart_kind == 'highcharts':
            d = get_highcharts_data(chart_klass, simple_data_source, options)
        elif chart_kind == 'c3js':
            d = get_c3_data(chart_klass, simple_data_source, options)
    else:
        d = {'chart_unspecific_data': data_list}
    d['title'] = options.get('title')
    return d

def get_formatted_data(data_source):
    if isinstance(data_source, list):
        return data_source
    else:
        try:
            data_list = data_source.values.tolist()
            data_list.insert(0, data_source.columns)
        except:
            engine = create_engine('postgresql://bodhi:allright@localhost:5432/bodhi_db')
            result = engine.execute(data_source)
            data_list = result.fetchall()
            data_list.insert(result.keys())
        return data_list
