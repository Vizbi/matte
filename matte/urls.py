from django.conf.urls import url
from .views import test_route_url

urlpatterns = [
    url(r'^(?P<url>[-\w]+)/$', test_route_url, name='test_route_url'),
]