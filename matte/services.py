from graphos.sources.simple import SimpleDataSource
from graphos.renderers.highcharts import LineChart


class Board():

    def __init__(self, storyboard):
        self.storyboard = storyboard

    def get_chart(self):
        data = [sc.data for sc in self.storyboard.saved_charts.all()]
        data_sources = [SimpleDataSource(data=each) for each in data]
        return [LineChart(data_source) for data_source in data_sources]

