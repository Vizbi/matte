from django.conf.urls import url
from matte.views import UrlRoute


urlpatterns = [
    url(r'^(?P<url>[-\w]+)/$', UrlRoute.as_view(), name='test_route_url'),
]
