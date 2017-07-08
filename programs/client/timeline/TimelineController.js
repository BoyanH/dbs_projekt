htViewerApp.controller('TimeLineController', ['$scope','$routeParams', '$location', function($scope, $routeParams, $location)  {
        
	$scope.selectedHashtag = $routeParams.selectedHashtag;
	$scope.usage = 'daily';

	$scope.hashtagSelected = function(ht) {
		$scope.selectedHashtag = ht;
		$location.path('/timeline/' + (ht || ''), false);
	}

	$scope.setUsage = function(newVal) {
		$scope.usage = newVal;
	}
}]);