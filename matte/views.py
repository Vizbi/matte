from django.shortcuts import render_to_response

from .models import Storyboard
from .services import Board
import matte.viz


def test_route_url(request, url):
    storyboard = Storyboard.objects.get(url=url)
    board = Board(storyboard)
    board = {'board': board.get_chart()}
    return render_to_response('matte/test.html', board)
