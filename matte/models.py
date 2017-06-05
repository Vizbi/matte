from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import crypto

from .services import get_formatted_data

NONE = 'None'
NOW = 'Now'
DAILY = 'Daily'
WEEKLY = 'Weekly'
MONTHLY = 'Monthly'

MINUTE = 'minute'
HOUR = 'hour'
DAY_OF_WEEK = 'day_of_week'
DAY_OF_MONTH = 'day_of_month'
EXPIRES = 'expires'

SCHEDULE_TIME_CHOICES = {
    DAILY: {MINUTE: '30', HOUR: '16', DAY_OF_WEEK: '*', DAY_OF_MONTH: '*'},
    WEEKLY: {
        MINUTE: '30', HOUR: '16', DAY_OF_WEEK: 'saturday', DAY_OF_MONTH: '*'
    },
    MONTHLY: {MINUTE: '30', HOUR: '16', DAY_OF_WEEK: '*', DAY_OF_MONTH: '1'}
}


class SelectControl(object):

    def __init__(self, controls):
        self.controls = controls

    def get_controls(self):
        return self.controls


class Visualization(object):
    _all = set()
    def __init__(self, data, name, chart_type='line', chart_kind='highcharts'):
        self.data = get_formatted_data(data)
        self.name = name
        self.chart_type = chart_type
        self.chart_kind = chart_kind
        self.__class__._all.add(self)

    def set_controls(self, controls):
        self.controls = controls.controls

class Storyboard(object):
    _all = set()
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.__class__._all.add(self)

    def set_visualizations(self, visualizations):
        self.visualizations = visualizations

    def get_visualizations(self):
        return self.visualizations
