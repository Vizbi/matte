from pandas import DataFrame
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

df = DataFrame(data[1:], columns=data[0])
query = 'Select "City", "Floors" from buildings'
viz = Visualization(data=data, name='viz 1', chart_type='bar')
viz.input_slider(2004, 2006)
viz1 = Visualization(data=data1, name='viz 2', chart_type='column')
viz2 = Visualization(data=data1, name='viz 3')
viz3 = Visualization(data=df, name='viz 3', chart_type='column')
viz4 = Visualization(data=query, name='viz 3')

storyboard = Storyboard(url='Sales-by-Year', title='Sales by year')
storyboard.set_visualizations([viz, viz1])

storyboard1 = Storyboard(url='this-is-a-test-url', title='Test title')
storyboard1.set_visualizations([viz])

storyboard2 = Storyboard(url='year-sales', title='Year Sales')
storyboard2.set_visualizations([viz1, viz2])

storyboard3 = Storyboard(url='dataframe-viz', title='Storyboard with Dataframe')
storyboard3.set_visualizations([viz3])

storyboard4 = Storyboard(url='sqlalchemy-viz', title='Storyboard with Sqlalchemy')
storyboard4.set_visualizations([viz4])

storyboard5 = Storyboard(url='mixed-viz', title='Storyboard ')
storyboard5.set_visualizations([viz2, viz3, viz4])
