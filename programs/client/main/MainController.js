htViewerApp.controller('MainController', function($scope, $location) {
        
	 $scope.isActive = function (viewLocation) { 
	 	console.log($location.path());
        return viewLocation === $location.path();
    };

});