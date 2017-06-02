from django.shortcuts import render
from pandas import DataFrame
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Storyboard
from .services import get_chart_specific_data, get_formatted_data
import matte.viz


def index(request):
    return render(request, 'index.html')


class UrlRoute(APIView):

    def get(self, request, url, *args, **kwargs):
        storyboard = [x for x in Storyboard._all if x.url == url][0]
        data = []
        for each in storyboard.get_visualizations():
            chart_data = get_chart_specific_data(each.data, each.chart_type, each.chart_kind)
            if hasattr(each, 'slider_enabled'):
                try:
                    slider = {
                        'min': each.slider_low_value,
                        'max': each.slider_high_value,
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

            chart_data['slider'] = slider
            data.append(chart_data)
        return Response(data)


class UpdatedChart(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params
        storyboard = [x for x in Storyboard._all if x.url == data['slug']][0]
        id = int(data['viz_id'])
        viz = storyboard.get_visualizations()[id]
        df = DataFrame(get_formatted_data(viz.data))
        df.columns = df.iloc[0]
        df.drop([0, ], inplace=True)
        df.set_index(df['Year'], inplace=True)
        new_df = df[df.index.isin(range(int(data['lowValue']), int(data['highValue']) + 1))]
        chart_data = new_df.values.tolist()
        chart_data.insert(0, new_df.columns.tolist())
        chart_data = get_chart_specific_data(chart_data, viz.chart_type, viz.chart_kind)
        return Response({'chartData': chart_data, 'id': data['viz_id']})



