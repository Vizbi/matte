(function () {
    "use strict";
    angular
        .module('header')
        .component('header', {
            'templateUrl': 'static/html/fixed-top.template.html',
            'controller': ['$location', function ($location) {
            }]
        });
}());
