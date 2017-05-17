from django.shortcuts import render_to_response

from .models import Storyboard, Visualization
from .services import Board


def test(request):
    data = [['Year', 'Department', 'Sales', 'Expenses'],
            [2004, 'Bikes', 1000, 400],
            [2005, 'Bikes', 1170, 460],
            [2006, 'Bikes', 660, 1120],
            [2007, 'Bikes', 1030, 540],
            [2004, 'Cars', 1000, 400],
            [2005, 'Cars', 1170, 460],
            [2006, 'Cars', 660, 1120],
            [2007, 'Cars', 1030, 540]]
    viz = Visualization.objects.create(data=data)
    viz1 = Visualization.objects.create(data=data)
    storyboard = Storyboard.objects.create(url='Sales-by-Year', title='Sales by year')
    storyboard.saved_charts.set([viz, viz1])
    storyboard.save()
    board = Board(storyboard)
    board = {'board': board.get_chart()}
    return render_to_response('matte/test.html', board)
