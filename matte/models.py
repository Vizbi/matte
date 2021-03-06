from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import crypto

User = settings.AUTH_USER_MODEL

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

    controls = JSONField()

    @property
    def get_controls(self):
        return self.controls


class Visualization(object):
    _all = set()
    def __init__(self, data, name, chart_type='line', chart_kind='highcharts'):
        self.data = data
        self.name = name
        self.chart_type = chart_type
        self.chart_kind = chart_kind
        self.__class__._all.add(self)

    def input_slider(self, low, high, enabled=True):
        self.slider_low_value = low
        self.slider_high_value = high
        self.slider_enabled = enabled

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
