(function () {
    "use strict";
    angular
        .module("core", ['ngSanitize'])
        .directive("renderVisualization", ["$rootScope", "$compile", "ChartDrawService", "CoreService", function ($rootScope, $compile, ChartDrawService, CoreService) {
            // At several places, we need to show a chart, or single value or table.
            // So we should be able to say something like
            // <render-visualization chart-data="item.chartData" uuid="item.uuid"></render-visualization>
            // uuid is needed because multiple charts might be needed on same page. So uuid tells the id in which chart will be rendered.
            return {
                restrict: 'E',
                link: function (scope, element, attrs) {
                    scope.$watch('chartData', function (newVal, oldVal) {
                        element.html('');
                        var isSingleValueVisualization;
                        var templateRendererScope;
                        var tabularData = scope.chartData && scope.chartData.chart_unspecific_data;
                        isSingleValueVisualization = scope.chartData && scope.chartData.single_value;
                        if (isSingleValueVisualization) {
                            element.html('<ng-include src="\'/static/html/single-value-visualization.template.html\'"></ng-include>');
                            templateRendererScope = $rootScope.$new();
                            templateRendererScope.heading = tabularData[0][0];
                            templateRendererScope.body = tabularData[1][0];
                            $compile(element.contents())(templateRendererScope);
                        }
                        else if (scope.chartData) {
                            if (scope.chartData.chartType === 'html') {
                                //element.html(tabularData);
                                element.html('<ng-include src="\'/static/html/html-text.template.html\'"></ng-include>');
                                templateRendererScope = $rootScope.$new();
                                templateRendererScope.ahtml = tabularData;
                                $compile(element.contents())(templateRendererScope);
                            }
                            else if (scope.chartData.chartType === 'table'){
                                element.html('<ng-include src="\'/static/html/table-renderer.template.html\'"></ng-include>');
                                templateRendererScope = $rootScope.$new();
                                templateRendererScope.tabularData = tabularData;
                                templateRendererScope.title = scope.chartData.title;
                                $compile(element.contents())(templateRendererScope);
                            }
                            else {
                                var boxContent = $('<div class="chart-content"></div>');
                                boxContent.attr('id', scope.uuid);
                                boxContent.appendTo(element);
                                var chartKind = CoreService.getChartKind();
                                ChartDrawService.drawChart(scope.chartData, chartKind, scope.chartData.chartType, scope.uuid);
                            }
                        }
                    });
                },
                scope: {
                    'chartData': '=',
                    'uuid': '=',
                    'chartType': '=',
                },
            };
        }]);
    angular
        .module("core")
        .directive("intercom", ['Intercom', 'AuthService', '$http', '$cookies', '$rootScope', function(Intercom, AuthService, $http, $cookies, $rootScope) {
          return {
            link: function(scope, element, attrs) {
              scope.$watch(function(){ return AuthService.user.loggedIn;}, function(user) {
              var userDetails ={};
              var dataFetch;
                if(Object.keys(AuthService.user).length > 1){
                   var config = { 'headers': { 'Authorization': "Token "+$cookies.get('token')} };
                    dataFetch = $http.get("user/details/", config).then(function(response){
                        userDetails.name = response.data.username;
                        userDetails.email =response.data.email;
                        var shaObj = new jsSHA('SHA-256', "TEXT");
                        shaObj.setHMACKey("WpYDdoFfY94HcnWibf86KZCgAvC8ZMbJZt3HW0Ie", "TEXT");
                        shaObj.update(userDetails.email);
                        userDetails.user_hash =shaObj.getHMAC('HEX');
                    });
                }
                if(dataFetch !== undefined){
                    dataFetch.then(function(){
                        Intercom.boot(userDetails);
                        Intercom.update();
                    });
                }else{
                    if($rootScope.enableIntercom){
                        Intercom.shutdown();
                        Intercom.boot(userDetails);
                        Intercom.update();
                    }
                }
              });
            }
          };
        }]);
    angular
        .module("core")
        .directive('setTitle', ['$document', function($document) {
            return {
                link: function(scope) {
                    $document[0].title = 'Vizbi' + ' - ' + scope.title;
                    // TODO: This shouldn't remove all classes of body.
                    // It should only loop through SBtemplateOptions classes and if any of that class is present on body then that should be removed.
                    // This logic should be moved out of setTitle and should be placed in $routeChangeStart
                    if($document[0].body.classList[0] !== undefined){
                        $document[0].body.classList.remove($document[0].body.classList[0]);
                    }
                },
                scope: {
                    'title': '@',
                },
            };
        }]);
}());
