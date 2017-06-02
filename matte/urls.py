from django.conf.urls import url
from matte.views import UrlRoute, UpdatedChart


urlpatterns = [
    url(r'^get-updated-chart/$', UpdatedChart.as_view(), name='get-updated-chart'),
    url(r'^(?P<url>[-\w]+)/$', UrlRoute.as_view(), name='route-url'),
]
