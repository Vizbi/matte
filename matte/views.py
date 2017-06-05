from django.shortcuts import render
from pandas import DataFrame
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Storyboard
from .services import get_chart_specific_data
import matte.viz

def index(request):
    return render(request, 'index.html')


class UrlRoute(APIView):

    def get(self, request, url, *args, **kwargs):
        storyboard = [x for x in Storyboard._all if x.url == url][0]
        data = []
        for each in storyboard.get_visualizations():
            chart_data = get_chart_specific_data(each.data, each.chart_type, each.chart_kind)
            filtered_data = get_filtered_data(each)
            filtered_chart_data = get_chart_specific_data(filtered_data, each.chart_type, each.chart_kind)

            if hasattr(each, 'controls') and each.controls['input_slider']:
                try:
                    slider = {
                        'min': each.controls['input_slider']['low_value'],
                        'max': each.controls['input_slider']['high_value'],
                        'options': {
                            'floor': int(min(chart_data['x_axis']['categories'])),
                            'ceil': int(max(chart_data['x_axis']['categories'])),
                            'interval': 1500
                        }
                    }
                except:
                    slider = {}
            else:
                slider = {}

            filtered_chart_data['slider'] = slider
            data.append(filtered_chart_data)
        return Response(data)


class UpdatedChart(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params
        storyboard = [x for x in Storyboard._all if x.url == data['slug']][0]
        id = int(data['viz_id'])
        viz = storyboard.get_visualizations()[id]
        df = DataFrame(viz.data)
        df.columns = df.iloc[0]
        df.drop([0, ], inplace=True)
        df.set_index(df.columns[0], inplace=True)
        new_df = df[df.index.isin(range(int(data['lowValue']), int(data['highValue']) + 1))]
        chart_data = new_df.values.tolist()
        chart_data.insert(0, new_df.columns.tolist())
        chart_data = get_chart_specific_data(chart_data, viz.chart_type, viz.chart_kind)
        return Response({'chartData': chart_data, 'id': data['viz_id']})


def get_filtered_data(viz):
    if hasattr(viz, 'controls') and viz.controls['input_slider']:
        df = DataFrame(viz.data)
        df.columns = df.iloc[0]
        df.drop([0, ], inplace=True)
        df.set_index(df.columns[0], inplace=True)
        if df.index.dtype != object:
            new_df = df[
                df.index.isin(range(viz.controls['input_slider']['low_value'],
                                    viz.controls['input_slider'][
                                            'high_value'] + 1))]
        else:
            df.reset_index(inplace=True)
            new_df = df
        chart_data = new_df.values.tolist()
        chart_data.insert(0, new_df.columns.tolist())
        return chart_data
    else:
        return viz.data


