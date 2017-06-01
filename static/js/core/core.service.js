(function () {
    "use strict";
    angular
        .module("core")
        .factory("CoreService", ["$http", function ($http) {

            function getChartKind () {
                // Right now it is hard coded but later we will store the selected chartKind in a variable and will return it from here.
                //return "c3js";
                return "highcharts";
            }

            return {
                getChartKind: getChartKind,
            };
        }]);
}());
