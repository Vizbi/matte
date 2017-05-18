from matte.models import Storyboard, Visualization


data = [['Year', 'Department', 'Sales', 'Expenses'],
        [2004, 'Bikes', 1000, 400],
        [2005, 'Bikes', 1170, 460],
        [2006, 'Bikes', 660, 1120],
        [2007, 'Bikes', 1030, 540],
        [2004, 'Cars', 1000, 400],
        [2005, 'Cars', 1170, 460],
        [2006, 'Cars', 660, 1120],
        [2007, 'Cars', 1030, 540]]
viz = Visualization.objects.create(data=data, name='viz 1')
viz1 = Visualization.objects.create(data=data, name='viz 2')
storyboard = Storyboard.objects.create(url='Sales-by-Year',
                                       title='Sales by year')
storyboard.saved_charts.set([viz, viz1])
storyboard.save()


storyboard1 = Storyboard.objects.create(url='this-is-a-test-url', title='Test title')
storyboard1.saved_charts.set([viz])
storyboard1.save()
