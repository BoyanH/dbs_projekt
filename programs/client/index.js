var htViewerApp = angular.module('htViewerApp', ['ngResource', 'ngRoute']);

console.log('angular added');

// configure our routes
htViewerApp.config(function($routeProvider, $locationProvider, $httpProvider) {

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl : '/public/main/main.html',
            controller  : 'MainController'
        })

        // route for the about page
        .when('/clustering/:selectedHashtag?', {
            templateUrl : '/public/clustering/clustering.html',
            controller  : 'ClusteringController'
        })

        // route for the contact page
        .when('/timeline/:selectedHashtag?', {
            templateUrl : '/public/timeline/timeline.html',
            controller  : 'TimeLineController',
            reloadOnSearch: false
        }).otherwise({redirectTo:'/'});

        // use the HTML5 History API
        $locationProvider.html5Mode(true);
});

htViewerApp.run(function($rootScope, $location){
    var history = [];

    $rootScope.$on('$routeChangeSuccess', function() {
        history.push($location.$$path);
    });
    $rootScope.history = history;
});

htViewerApp.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
    var original = $location.path;
    $location.path = function (path, reload) {
        if (reload === false) {
            var lastRoute = $route.current;
            var un = $rootScope.$on('$locationChangeSuccess', function () {
                $route.current = lastRoute;
                un();
            });
        }
        return original.apply($location, [path]);
    };
}])