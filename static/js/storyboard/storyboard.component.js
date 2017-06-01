(function () {
    "use strict";
    angular
        .module('storyboard')
        .component('storyboard', {
            'templateUrl': 'static/html/storyboard.template.html',
            'controller': ['$scope', '$http', '$window', '$location', '$routeParams', 'StoryboardService', function ($scope, $http, $window, $location, $routeParams, StoryboardService) {
                var slug = $routeParams.storyboardSlug;
                var self = this;
                StoryboardService.setStoryboardUrl(slug);
                $http.get('matte/' + slug).then(function(response) {
                    var i = 0;
                    StoryboardService.setChartData(response.data);
                    self.chartData = StoryboardService.getChartData()
                }, function(response) {
                    debugger;
                });
                $scope.$watch(function () {
                        return StoryboardService.getChartData();
                    },
                    function () {
                        self.chartData = StoryboardService.getChartData();
                    });
            }]
        });
}());
