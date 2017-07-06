htViewerApp.controller('ClusteringController', function($scope) {
        
	// add code, export variables in templates via $scope
	console.log('Main controller loaded')

	$scope.asd = 2;


	setTimeout(function() {

		$scope.asd = 3;
		$scope.$apply();
	}, 1000)

});