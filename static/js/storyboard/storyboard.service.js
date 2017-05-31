(function () {
    "use strict";
    angular
        .module("storyboard")
        .factory("StoryboardService", ["$http", function ($http) {
            var chartData = {};
            var slug = null;
            var getChartData = function () {
                return chartData;
            }
            var setStoryboardUrl = function (url) {
                slug = url;
            }
            var getStoryboardUrl = function () {
                return chartData;
            }
            var n_test = function (lowValue, highValue, id) {
                chartData[id].slider.range = lowValue + '-' + highValue;
                var title = chartData[id].x_axis.title.text
                $http({
                    url: '/matte/get-updated-chart',
                    method: 'GET',
                    params: {
                        lowValue: lowValue, highValue: highValue,
                        slug: slug, viz_id: id, title: title
                    }
                }).then(function (response) {
                    setChartData(response.data.chartData, response.data.id)
                }, function (response) {
                });
            };
            var test = function (sliderId, modelValue, highValue, pointerType) {
                n_test(modelValue, highValue, sliderId);
            };
            var setChartData = function (val, id) {
                if (id == undefined) {
                    chartData = val;
                }
                else {
                    var vizSlider = chartData[id].slider;
                    chartData[id] = val;
                    chartData[id].slider = vizSlider;
                }
                var i = 0;
                angular.forEach(chartData, function (data) {
                    if (!angular.equals(data.slider, {})) {
                        data['slider']['options']['onChange'] = test;
                        data['slider']['options']['id'] = i++;
                        data['slider']['range'] = data.slider.min + '-' + data.slider.max;
                    }
                });
            }
            var setVisualizationData = function (vizData, id) {
                chartData[id] = vizData;
            }
            return {
                getChartData: getChartData,
                setStoryboardUrl: setStoryboardUrl,
                getStoryboardUrl: getStoryboardUrl,
                setChartData: setChartData,
                setVisualizationData: setVisualizationData
            }
        }]);
}());