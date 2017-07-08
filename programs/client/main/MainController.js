htViewerApp.controller('MainController', function($scope, $location) {
        
	 $scope.isActive = function (viewLocation) { 
        return $location.path().indexOf(viewLocation) > -1;
    };

});