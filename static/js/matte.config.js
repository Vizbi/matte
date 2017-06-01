(function () {
    "use strict";
    angular.
    module('matteApp').
    config(['$locationProvider', '$routeProvider',
        function config($locationProvider, $routeProvider) {
            $locationProvider.hashPrefix('!');

            $routeProvider.
            when('/', {
                templateUrl: 'static/html/home.template.html'
            }).
            when('/:storyboardSlug', {
                template: '<storyboard></storyboard>'
            }).
            otherwise('/');
        }]).
    run(['$rootScope', '$http', '$location', function ($rootScope, $http, $location) {
        $rootScope.$on('$routeChangeStart', function (event) {
            $rootScope.enableHeader = true;
            $rootScope.enableFooter = false;
        });
    }]);
}());
