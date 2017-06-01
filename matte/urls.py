from django.conf.urls import url
from matte.views import UrlRoute, GetUpdatedChart


urlpatterns = [
    url(r'^get-updated-chart/$', GetUpdatedChart.as_view(), name='get-updated-chart'),
    url(r'^(?P<url>[-\w]+)/$', UrlRoute.as_view(), name='route-url'),
]
