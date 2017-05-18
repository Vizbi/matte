from django.conf.urls import url
from django.shortcuts import render_to_response

from .models import Storyboard
from .services import Board


def test_route_url(request, url):
    storyboard = Storyboard.objects.get(url=url)
    board = Board(storyboard)
    board = {'board': board.get_chart()}
    return render_to_response('matte/test.html', board)


urlpatterns = [
    url(r'^(?P<url>[-\w]+)/$', test_route_url, name='test_route_url'),
]