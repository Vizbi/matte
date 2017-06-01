(function () {
    "use strict";
    angular
        .module('core')
        .factory('ChartDrawService', [function () {
            // This function assumes that correct attributes are set on data.
            // For highcharts, it assumes that data would have an attribute called categories
            // For c3, it assumes that data would have an attribute called c3data
            var drawChart = function (data, chartKind, chartType, div) {
                if (chartKind == 'highcharts') {
                    if (chartType == 'map'){
                            var loadScript = function ( mapArea, callback ) {
                              var d = {
                                'custom/world': 'static/js/highcharts/world.js',
                                'countries/in/custom/in-all-disputed': 'static/js/highcharts/in-all-disputed.js',
                                'countries/us/custom/us-all-territories': 'static/js/highcharts/us-all-territories.js',
                                'custom/asia': 'static/js/highcharts/asia.js',
                                'custom/benelux': 'static/js/highcharts/benelux.js',
                                'custom/british-isles': 'static/js/highcharts/british-isles.js',
                                'custom/british-isles-all': 'static/js/highcharts/british-isles.js',
                                'custom/usa-and-canada': 'static/js/highcharts/usa-and-canada.js',
                                'custom/central-america': 'static/js/highcharts/central-america.js',
                                'custom/europe': 'static/js/highcharts/europe.js',
                                'custom/european-union': 'static/js/highcharts/european-union.js',
                                'custom/middle-east': 'static/js/highcharts/middle-east.js',
                                'custom/nordic-countries-core': 'static/js/highcharts/nordic-countries-core.js',
                                'custom/nordic-countries': 'static/js/highcharts/nordic-countries.js',
                                'custom/north-america-no-central': 'static/js/highcharts/north-america-no-central.js',
                                'custom/north-america': 'static/js/highcharts/north-america.js',
                                'custom/nato': 'static/js/highcharts/nato.js',
                                'custom/oceania': 'static/js/highcharts/oceania.js',
                                'custom/scandinavia': 'static/js/highcharts/scandinavia.js',
                                'custom/south-america': 'static/js/highcharts/south-america.js',
                                'custom/world-continents': 'static/js/highcharts/world-continents.js',
                                'custom/world-palestine-highres': 'static/js/highcharts/world-palestine-highres.js',
                                'custom/world-palestine-lowres': 'static/js/highcharts/world-palestine-lowres.js',
                                'custom/world-palestine': 'static/js/highcharts/world-palestine.js',
                                'custom/world-eckert3-highres': 'static/js/highcharts/world-eckert3-highres.js',
                                'custom/world-eckert3': 'static/js/highcharts/world-eckert3.js',
                                'custom/world-highres': 'static/js/highcharts/world-highres.js',
                                'custom/world-lowres': 'static/js/highcharts/world-lowres.js',
                                'custom/world-highres2': 'static/js/highcharts/world-highres2.js',
                                'custom/world-highres3': 'static/js/highcharts/world-highres3.js',
                                'custom/world-robinson-highres': 'static/js/highcharts/world-robinson-highres.js',
                                'custom/world-robinson-lowres': 'static/js/highcharts/world-robinson-lowres.js',
                                'custom/world-robinson': 'static/js/highcharts/world-robinson.js',
                                'countries/af-all': 'static/js/highcharts/af-all.js',
                                'countries/in-all-disputed': 'static/js/highcharts/in-all-disputed.js',
                                'countries/us-all-territories': 'static/js/highcharts/us-all-territories.js',
                                'countries/in/up-all': 'static/js/highcharts/india-up.js',
                                'countries/in/up-constituencies': 'static/js/highcharts/india-up-constituencies.js',
                                'countries/in/punjab-constituencies': 'static/js/highcharts/india-punjab-constituencies.js',
                                'countries/in/goa-constituencies': 'static/js/highcharts/india-goa-constituencies.js',
                                'countries/in/manipur-constituencies': 'static/js/highcharts/india-manipur-constituencies.js',
                                'countries/in/uk-constituencies': 'static/js/highcharts/india-uttarakhand-constituencies.js',
							};
                            $script([d[mapArea]], function () {
                                callback();
                            });
						};

						var mapArea = data.map_area;
						loadScript(mapArea, function() {
							var data_series = angular.copy(data.data_series);
							var series_name = data.series_name;
							var po = data.plot_options;
							po.map.mapData = Highcharts.maps[data.map_area];
							po.mapbubble.mapData = Highcharts.maps[data.map_area];
							var highchartsObj = {
								title: {
									text: data.title
								},
                                subtitle: {
                                    text: data.subtitle
                                },
								exporting: {
									enabled: data.downloadable || false
								},
                                legend: data.legend || {},
                                tooltip: data.tooltip || {},
								credits: data.credits,
                                chart: data.chart || {},
								colorAxis: data.color_axis,
                                series: data_series,
								plotOptions: po
							};
							if (data.series_type == 'multi_series' || data.map_type == 'mapbubble') {
							    delete highchartsObj.colorAxis;
							}
                            if (data.series_type == 'multi_series' && data.map_type == 'map') {
                                po.map.nullColor = 'rgba(0,0,0,0)';
                            }
							$('#'+div).highcharts('Map', highchartsObj);
						});
                    }
                    else {
                        var highchartsObj = {
                            title: {
                                text: data.title
                            },
                            subtitle: {
                                text: data.subtitle
                            },
                            exporting: {
                                enabled: data.downloadable || false
                            },
                            legend: data.legend || {},
                            tooltip: data.tooltip || {},
                            credits: data.credits,
                            xAxis: data.x_axis,
                            yAxis: data.y_axis || {},
                            chart: data.chart || {},
                            plotOptions: data.plot_options || {},
                            series: data.data_series,
                        };
                        if (chartType == 'heatmap') {
                            highchartsObj.colorAxis = data.color_axis;
                        }
                        $('#'+div).highcharts(highchartsObj);
                    }
                }
                else if (chartKind == 'c3js') {
                    if (chartType == 'pie') {
                        c3.generate({
                            bindto: document.getElementById(div),
                            data: {
                                columns: data.c3data,
                                type: chartType
                            }
                        });
                    }
                    else if (chartType == 'column') {
                        c3.generate({
                            bindto: document.getElementById(div),
                            data: {
                                x: data.x_axis_title,
                                columns: data.c3data,
                                type: 'bar'
                            },
                            axis: {
                                x: {
                                    type: 'categorized'
                                },
                                rotated: true,
                            }
                        });
                    }
                    else if (chartType == 'donut') {
                        c3.generate({
                            bindto: document.getElementById(div),
                            data: {
                                columns: data.c3data,
                                type: chartType
                            },
                            donut: {
                                title: data.title
                            }
                        });
                    }
                    else {
                        c3.generate({
                            bindto: document.getElementById(div),
                            data: {
                                x: data.x_axis_title,
                                columns: data.c3data,
                                type: chartType
                            },
                            axis: {
                                x: {
                                    type: 'categorized'
                                }
                            }
                        });
                    }
                }
            };

            return {
                drawChart: drawChart,
            };
        }]);
}());
