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


class SelectControl(models.Model):

    controls = JSONField()

    @property
    def get_controls(self):
        return self.controls


class Visualization(models.Model):
    data = JSONField(null=True, blank=True)
    raw_query = models.TextField(null=True, blank=True)
    uuid = models.CharField(max_length=20, unique=True,
                            default=crypto.get_random_string)
    # chart_type should be set to 'html' if raw_html is set
    chart_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    options = JSONField(null=True, blank=True)
    controls = models.OneToOneField(SelectControl, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def set_controls(self, controls):
        self.controls = controls


class Storyboard(models.Model):
    """
    Example:
    [[{u'chart_id': 4, u'span': u'col-md-12'}],
     [{u'chart_id': 5, u'span': u'col-md-12'}],
     [{u'chart_id': 6, u'span': u'col-md-12'}]]
    """
    PRIVATE = 'pri'
    ORGANIZATION = 'org'
    PUBLIC = 'pub'
    VISIBILITY_CHOICES = (
        (PRIVATE, 'Private'),
        (ORGANIZATION, 'Organization'),
        (PUBLIC, 'Public'),
    )
    BASIC = 'Basic'
    COMPACT = 'Compact'
    FIRE = 'fire_skin'
    EARTH = 'earth_skin'
    FOREST = 'forest_skin'
    TEMPLATE_CHOICES = (
        (BASIC, 'Basic'),
        (COMPACT, 'Compact'),
        (FIRE, 'fire_skin'),
        (EARTH, 'earth_skin'),
        (FOREST, 'forest_skin'),
    )

    uuid = models.CharField(max_length=20, unique=True,
                            default=crypto.get_random_string)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    saved_charts = models.ManyToManyField(Visualization)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES,
                                  default=PRIVATE)
    template_type = models.CharField(max_length=15, choices=TEMPLATE_CHOICES,
                                     default=BASIC)
    extra_emails = models.CharField(max_length=300, blank=True, null=True)

    def get_absolute_url(self):
        return "/db/storyboard/%s/" % self.uuid


    def get_frontend_absolute_url(self):
        return "/storyboards/%s/" % self.uuid

    def __unicode__(self):
        return self.title
