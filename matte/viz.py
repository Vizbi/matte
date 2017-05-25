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

data1 = [['Year', 'Department', 'Sales', 'Expenses'],
        [2004, 'Bikes', 100, 400],
        [2005, 'Bikes', 200, 460],
        [2006, 'Bikes', 300, 1120],
        [2007, 'Bikes', 400, 540],
        [2004, 'Cars', 500, 400],
        [2005, 'Cars', 600, 460],
        [2006, 'Cars', 700, 1120],
        [2017, 'Cars', 80, 50]]

viz = Visualization(data=data, name='viz 1', chart_type='bar')
viz1 = Visualization(data=data1, name='viz 2', chart_type='column')
viz2 = Visualization(data=data1, name='viz 3')
storyboard = Storyboard(url='Sales-by-Year', title='Sales by year')
storyboard.set_visualizations([viz, viz1])


storyboard2 = Storyboard(url='year-sales', title='Year Sales')
storyboard2.set_visualizations([viz1, viz2])


storyboard1 = Storyboard(url='this-is-a-test-url', title='Test title')
storyboard1.set_visualizations([viz])
