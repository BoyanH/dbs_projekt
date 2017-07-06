var htViewerApp = angular.module('htViewerApp', ['ngResource', 'ngRoute']);

console.log('angular added');

// configure our routes
htViewerApp.config(function($routeProvider) {

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl : '/public/main/main.html',
            controller  : 'MainController'
        })

        // route for the about page
        .when('/clustering', {
            templateUrl : '/public/clustering/clustering.html',
            controller  : 'ClusteringController'
        })

        // route for the contact page
        .when('/timeline', {
            templateUrl : '/public/timeline/timeline.html',
            controller  : 'TimeLineController'
        }).otherwise({redirectTo:'/'});
});

htViewerApp.run(function($rootScope, $location){
    console.log('app run');
    var history = [];

    $rootScope.$on('$routeChangeSuccess', function() {
        console.log('root changed');
        history.push($location.$$path);
    });
    $rootScope.history = history;
});