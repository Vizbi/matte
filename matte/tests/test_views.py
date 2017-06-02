from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from matte.models import Storyboard, Visualization
from matte.views import UrlRoute, UpdatedChart


class TestUrlRouteView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UrlRoute.as_view()
        data = [['Year', 'Sales', 'Expenses'],
                [2004, 1, 5],
                [2005, 2, 10],
                [2006, 3, 15],
                [2007, 4, 20],
                [2004, 5, 25],
                [2005, 6, 30],
                [2006, 7, 35],
                [2007, 8, 40]]
        self.viz1 = Visualization(data=data, name='viz 1', chart_type='bar')
        self.viz2 = Visualization(data=data, name='viz 2')
        self.storyboard = Storyboard(url='Test-Storyboard', title='Test Storyboard')
        self.storyboard.set_visualizations([self.viz1, self.viz2])
        self.url = reverse('route-url', kwargs={'url': 'Test-Storyboard'})

    def test_get(self):
        request = self.factory.get(self.url)
        force_authenticate(request)
        response = self.view(request, 'Test-Storyboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(sorted(response.data[0].keys()),
                         sorted(['data_series', 'title', 'subtitle', 'plot_options',
                          'y_axis', 'x_axis', 'chart', 'credits', 'legend',
                          'tooltip', 'slider']))

    def test_input_slider_only_available_when_set(self):
        self.viz1.input_slider(2004, 2006)
        request = self.factory.get(self.url)
        force_authenticate(request,)
        response = self.view(request, 'Test-Storyboard')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0]['slider'], {})
        self.assertEqual(response.data[1]['slider'], {})

    def test_input_slider_values_are_correct(self):
        self.viz1.input_slider(2004, 2006)
        request = self.factory.get(self.url)
        force_authenticate(request,)
        response = self.view(request, 'Test-Storyboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['slider']['min'], 2004)
        self.assertEqual(response.data[0]['slider']['max'], 2006)

    def test_response_data(self):
        data = [{
            "data_series": [{
                "name": "Sales",
                "data": [1, 2, 3, 4, 5, 6, 7, 8]
            }, {
                "name": "Expenses",
                "data": [5, 10, 15, 20, 25, 30, 35, 40]
            }], "title": None, "subtitle": None,
            "plot_options": {}, "y_axis": {"title": {"text": "Values"}},
            "x_axis": {
                "categories": [2004, 2005, 2006, 2007, 2004, 2005, 2006, 2007],
                "title": {"text": "Year"}
            }, "chart": {"type": "bar"}, "credits": {"enabled": False},
            "legend": {}, "tooltip": {}, "slider": {
                "min": 2004, "max": 2006,
                "options": {"floor": 2004, "ceil": 2007, "interval": 1500}
            }
        }, {
            "data_series": [{
                "name": "Sales",
                "data": [1, 2, 3, 4, 5, 6, 7, 8]
            }, {
                "name": "Expenses",
                "data": [5, 10, 15, 20, 25, 30, 35, 40]
            }], "title": None, "subtitle": None,
            "plot_options": {}, "y_axis": {"title": {"text": "Values"}},
            "x_axis": {
                "categories": [2004, 2005, 2006, 2007, 2004, 2005, 2006, 2017],
                "title": {"text": "Year"}
            }, "chart": {"type": "line"}, "credits": {"enabled": False},
            "legend": {}, "tooltip": {}, "slider": {}
        }]
        self.viz1.input_slider(2004, 2006)
        request = self.factory.get(self.url)
        force_authenticate(request,)
        response = self.view(request, 'Test-Storyboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1]['chart'], data[1]['chart'])


class TestUpdatedChartView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UpdatedChart.as_view()
        data = [['Year', 'Sales', 'Expenses'],
                [2004, 1, 5],
                [2005, 2, 10],
                [2006, 3, 15],
                [2007, 4, 20],
                [2004, 5, 25],
                [2005, 6, 30],
                [2006, 7, 35],
                [2007, 8, 40]]
        self.viz1 = Visualization(data=data, name='viz 1', chart_type='bar')
        self.viz2 = Visualization(data=data, name='viz 2')
        self.storyboard = Storyboard(url='Test-Storyboard', title='Test Storyboard')
        self.storyboard.set_visualizations([self.viz1, self.viz2])
        self.url = reverse('route-url', kwargs={'url': 'Test-Storyboard'})

    def test_get(self):
        request = self.factory.get(self.url,  {'viz_id': 1, 'lowValue':2005, 'highValue': 2007, 'slug': 'Test-Storyboard' })
        force_authenticate(request)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_only_given_range_is_present_in_response(self):
        request = self.factory.get(self.url,  {'viz_id': 1, 'lowValue':2005, 'highValue': 2007, 'slug': 'Test-Storyboard' })
        force_authenticate(request)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        print(response.data.keys())
        self.assertEqual(set(response.data['chartData']['x_axis']['categories']), set(range(2005, 2007 + 1)))
