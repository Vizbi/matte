import json
from django.shortcuts import render_to_response
from graphos.renderers.c3js import BarChart as C3BarChart
from graphos.renderers.c3js import ColumnChart as C3ColumnChart
from graphos.renderers.c3js import LineChart as C3LineChart
from graphos.renderers.c3js import PieChart as C3PieChart
from graphos.renderers.highcharts import AreaChart as HighchartsAreaChart
from graphos.renderers.highcharts import BarChart as HighchartsBarChart
from graphos.renderers.highcharts import Bubble
from graphos.renderers.highcharts import ColumnChart as HighchartsColumnChart
from graphos.renderers.highcharts import \
    ColumnLineChart as HighChartColumnLineChart
from graphos.renderers.highcharts import DonutChart as HighchartsDonutChart
from graphos.renderers.highcharts import Funnel
from graphos.renderers.highcharts import HeatMap
from graphos.renderers.highcharts import HighMap
from graphos.renderers.highcharts import LineChart as HighchartsLineChart
from graphos.renderers.highcharts import \
    LineColumnChart as HighChartLineColumnChart
from graphos.renderers.highcharts import \
    MultiAxisChart as HighChartMultiAxisChart
from graphos.renderers.highcharts import PieChart as HighchartsPieChart
from graphos.renderers.highcharts import PieDonut
from graphos.renderers.highcharts import ScatterChart as HighchartsScatterChart
from graphos.renderers.highcharts import TreeMap
from graphos.sources.simple import SimpleDataSource

from .models import Storyboard, Visualization
from .services import Board

chart_klasses = {}
chart_klasses['highcharts'] = {
    'line': HighchartsLineChart,
    'bar': HighchartsBarChart,
    'column': HighchartsColumnChart,
    'pie': HighchartsPieChart,
    'donut': HighchartsDonutChart,
    'area': HighchartsAreaChart,
    'scatter': HighchartsScatterChart,
    'dual_axis': HighChartMultiAxisChart,
    'line_column': HighChartLineColumnChart,
    'column_line': HighChartColumnLineChart,
    'map': HighMap,
    'heatmap': HeatMap,
    'funnel': Funnel,
    'treemap': TreeMap,
    'piedonut': PieDonut,
    'bubble': Bubble
}
chart_klasses['c3js'] = {
    'line': C3LineChart,
    'bar': C3BarChart,
    'column': C3ColumnChart,
    'pie': C3PieChart,
}


class ChartData():
    """
    """

    def __init__(self, storyboard):
        self.storyboard = storyboard

    def test(self):
        sc = self.storyboard.saved_charts.first()
        data = sc.data
        chart_specific_data = get_chart_specific_data(data, 'bar', 'highcharts')
        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = HighchartsLineChart(data_source)
        context = {'chart': chart}
        return render_to_response('matte/test.html', context)


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


def get_visualization_and_data(visualization,
                               selected_visualization_variables={}):
    """
    This returns chartable data for a visualization.
    This will always fetch the chartable data from db. Caller should check in cache before calling this function.
    This doesn't apply ipython notebook transformation, and has nothing to do with ipython.
    """
    data = {}
    if visualization.user_database.db_engine == 'bigquery' and visualization.chart_type != 'html':
        app = Application.objects.get(name='bigquery')
        access_token = AccessToken.objects.get(application=app,
                                               user=visualization.user)
        refresh_token = RefreshToken.objects.get(access_token=access_token)
        oauth_cred = Credentials(token=access_token.token,
                                 refresh_token=refresh_token.token,
                                 token_uri='https://accounts.google.com/o/oauth2/token',
                                 client_id=app.client_id,
                                 client_secret=app.client_secret)
        bq = bigquery.Client(project=settings.BIGQUERY_PROJECT_NAME,
                             credentials=oauth_cred)
        query = bq.run_sync_query(visualization.raw_query)
        query.run()
        data = query.rows
        first_row = [field.name for field in query.schema]
        # TODO: Use append, not insert
        data.insert(0, first_row)
    else:
        if visualization.measure_infos or visualization.dimension_infos:
            visualization_variable_ids = selected_visualization_variables.keys()
            # Find VisualizationVariables related to this Visualization
            variables = visualization.visualizationvariable_set.filter(
                id__in=visualization_variable_ids)
            variables_dict = {}
            for visualization_variable in variables:
                variables_dict[visualization_variable.name] = \
                selected_visualization_variables[str(visualization_variable.id)]
            database = Database(user_database=visualization.user_database,
                                dimension_infos=visualization.dimension_infos,
                                measure_infos=visualization.measure_infos,
                                visualization_variables=variables_dict)
            data = database.get_chartable_data(visualization.extra_filters)
        elif visualization.raw_query:
            database = Database(user_database=visualization.user_database)
            data = database.get_chartable_data_for_query(
                visualization.raw_query)
        elif visualization.raw_html:
            data = visualization.raw_html
    return visualization, data


def get_highcharts_data(chart_klass, data_source, options={}):
    # Clean options
    if 'colors' in options:
        options['colors'] = options['colors'].split(',')
    # Clean options
    chart = chart_klass(data_source, options=options)
    highcharts_data = {
        'data_series': chart.get_series(),
        'title': options.get('title'),
        'subtitle': options.get('subtitle'),
        'plot_options': chart.get_plot_options(),
        'y_axis': chart.get_y_axis(),
        'x_axis': chart.get_x_axis(),
        'chart': chart.get_chart(),
        'credits': chart.get_credits(),
        'legend': chart.get_legend(),
        'tooltip': chart.get_tooltip()
    }
    if highcharts_data['credits'] == {}:
        highcharts_data['credits'] = {'enabled': False}
    if chart_klass == HighMap:
        del highcharts_data['x_axis']
        del highcharts_data['y_axis']
        highcharts_data.update({
                                   'map_area': chart.get_map(),
                                   'color_axis': chart.get_color_axis(),
                                   'series_type': chart.series_type,
                                   'map_type': chart.get_chart_type()
                               })
    if chart_klass == HeatMap:
        highcharts_data.update({'color_axis': chart.get_color_axis()})
    return highcharts_data


def get_c3_data(chart_klass, data_source, options=None):
    chart = chart_klass(data_source, options=options)
    c3_data = {
        'title': chart.get_options().get('title'),
        'x_axis_title': chart.get_x_axis_title(),
    }
    if chart_klass is C3PieChart:
        chart_data = json.loads(chart.get_data())
    else:
        chart_data = json.loads(chart.get_columns_data())
    c3_data.update({'c3data': chart_data})
    return c3_data


def get_chart_specific_data(data, chart_type, chart_kind, options={}):
    """
    Arguments:
    data: [[]]: A list of lists. This should be in the format usable by SimpleDataSource
    chart_type: Whether we want line, or bar, or column etc.
    chart_kind: Whether highcharts or c3

    Returns:
    {}: Dictionary: Keys of returned dictionary will differ based on chart_type and chart_kind.
        For highcharts, this dictionary must contain x_axis_title, categories, data_series etc.
        For c3js, this dictionary must contain c3data, x_axis_title etc.

    This assumes that only supported chart_type and chart_kind will be passed.
    """
    if chart_type != 'table':
        simple_data_source = SimpleDataSource(data)
        chart_klass = get_chart_klass(chart_kind, chart_type)
        if chart_kind == 'highcharts':
            d = get_highcharts_data(chart_klass, simple_data_source, options)
        elif chart_kind == 'c3js':
            d = get_c3_data(chart_klass, simple_data_source, options)
    else:
        d = {'chart_unspecific_data': data}
    d['title'] = options.get('title')
    return d


def compute_chartable_data(visualization, dataframe):
    """
    This applies ipython notebook transformation on chartable_data of a visualization and stores result in a file. Notebook transformation must be applied on a docker container, so that it can't destroy/dirty the application server.
    Can't return anything from this function because I haven't yet found a way to get the response back from a docker container.

    Implementation details:
    Start a docker container based on a docker image.
    The docker container runs the notebook file and writes the output at some shared volume.
    The notebook file should be populated with latest dataframe before being run on docker container.

    1. Create the notebook file. This notebook file contains updated dataframe and a variable called output.
    2. Copy this notebook file to a shared volume.
    3. Create a docker container which does the following.
        - It should be able to run a python progam, so base image should be python.
        - Copy notebook_executor to container. This python script should read the ipython notebook name from an env variable.
        - Run ipython notebook
        - Write output to a shared volume
    4. Add a python script. This script should accept a notebook filename as argument and run the notebook. Also it should store the output on some shared volume.
    """
    # Read notebook
    notebook_name = visualization.notebook_name
    random_string = notebook_name.split('.')[0]

    # Update pickle file
    pickle_filename = random_string + '.pickle.txt'
    pickle_file_path = os.path.join(settings.NOTEBOOK_DIR,
                                    visualization.user.username,
                                    pickle_filename)
    with open(pickle_file_path, 'w') as f:
        pickle.dump(dataframe, f)

    # Pickle dump the output after running the notebook.
    ipy_fname = os.path.join(settings.NOTEBOOK_DIR, visualization.user.username,
                             notebook_name)
    nb = nbf.read(ipy_fname, 4)
    result_file = '/outputs/' + notebook_name + '_out'
    cc1 = "f = open('{0}', 'w')".format(result_file, )
    nb['cells'].append(nbf.v4.new_code_cell(cc1))
    cc2 = "pickle.dump(output, f)"
    nb['cells'].append(nbf.v4.new_code_cell(cc2))
    cc3 = "f.close()"
    nb['cells'].append(nbf.v4.new_code_cell(cc3))

    # Write notebook with print(output) appended
    output_fname = os.path.join(settings.RECOMPUTED_NOTEBOOK_DIR,
                                visualization.user.username, notebook_name)
    if not os.path.exists(os.path.dirname(output_fname)):
        try:
            os.makedirs(os.path.dirname(output_fname))
        except OSError:
            raise
    with open(output_fname, 'w') as f:
        nbf.write(nb, f)

    # Copy notebook, pickle file and python script on docker container.
    # Output pickle file will be different everytime this function runs.
    # Put the notebook in some shared volume and pass the filename to the container as env variable.
    # docker run --rm -it -v ~/recomputed-notebooks/akshar/Gaix1S9sip2T.ipynb:/code/Gaix1S9sip2T.ipynb -v ~/notebooks/akshar/Gaix1S9sip2T.pickle.txt:/code/Gaix1S9sip2T.pickle.txt -v ~/notebook-outputs/akshar/:/outputs/ -e NOTEBOOK_NAME=Gaix1S9sip2T.ipynb notebook_runner

    # This part should probably be done in celery, probably some other parts of this function too.
    if settings.DEBUG:
        os.environ['DOCKER_HOST'] = "tcp://192.168.99.100:2376"
        os.environ['DOCKER_TLS_VERIFY'] = '1'
        os.environ[
            'DOCKER_CERT_PATH'] = '/Users/akshar/.docker/machine/machines/default'
        cli = Client(version='auto', **kwargs_from_env())
    else:
        cli = Client(base_url='unix://var/run/docker.sock')
    environment = {'NOTEBOOK_NAME': notebook_name}
    binds = {}
    binds[output_fname] = {
        'bind': '/code/{0}'.format(notebook_name, ), 'mode': 'rw'
    }
    binds[pickle_file_path] = {
        'bind': '/code/{0}'.format(pickle_filename, ), 'mode': 'rw'
    }
    output_dir = os.path.join(settings.NOTEBOOK_OUTPUT_DIR,
                              visualization.user.username)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError:
            raise
    binds[output_dir] = {'bind': '/outputs', 'mode': 'rw'}
    volumes = ['/code/{0}'.format(notebook_name, ),
               '/code/{0}'.format(pickle_filename, ), '/outputs']
    resp = cli.create_container('notebook_runner', environment=environment,
                                host_config=cli.create_host_config(binds=binds),
                                volumes=volumes)
    if resp['Id']:
        cli.start(resp['Id'])


def get_chart_klass(chart_kind, chart_type):
    return chart_klasses[chart_kind][chart_type]
