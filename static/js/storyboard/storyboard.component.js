(function () {
    "use strict";
    angular
        .module('storyboard')
        .component('storyboard', {
            'templateUrl': 'static/html/storyboard.template.html',
            'controller': ['$http', '$window', '$location', '$routeParams', function ($http, $window, $location, $routeParams) {
                var slug = $routeParams.storyboardSlug;
                var self = this;
                $http.get('matte/' + slug).then(function(response) {
                    var i = 0;
                    self.chartData = response.data;
                }, function(response) {
                    debugger;
                });


            }]
        });
}());
