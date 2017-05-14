Matte will allow you build interactive web based data analysis with Python
, and with no knowledge of html, css and js. It is inspired by Shiny for R.
It uses Django, but knowledge of Django is not required to

Usage
----------

The simplest matte page looks like this


    # viz.py
    from matte import viz
    from matte import Storyboard, Visualization, SelectControl
    data =  [
        ['Year', 'Department', 'Sales', 'Expenses'],
        [2004, 'Bikes', 1000, 400],
        [2005, 'Bikes', 1170, 460],
        [2006, 'Bikes', 660, 1120],
        [2007, 'Bikes', 1030, 540],
        [2004, 'Cars', 1000, 400],
        [2005, 'Cars', 1170, 460],
        [2006, 'Cars', 660, 1120],
        [2007, 'Cars', 1030, 540]
    ]
    storyboard = Storyboard(url="Sales-by-Year", title='sales by year')
    control = SelectControl(["Bike", "Cars"])
    visualiztaion = Visualization(data=data)
    visualizations.set_controls({"Department": control})
    storyboard.add_visualization(visualiztaion)
    viz.add(storyboard)

Now run `python manage.py runserver` and access your interactive page at
`localhost:8000/Sales-by-Year`


Data sources
--------------

The data passed to a `Visualization` objects can be one of

1. A nested lists
2. A pandas dataframe
3. An sqlaclhemy queryset

Renderers
------------

Matte can use any of the reenderers defined in `Django-Graphos`. Google charts is the default reenderer.


Inspirations
---------------

1. https://shiny.rstudio.com/
2. https://github.com/plotly/dash
3. https://github.com/stitchfix/pyxley


