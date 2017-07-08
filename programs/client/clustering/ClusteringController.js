htViewerApp.controller('ClusteringController', ['$scope','$routeParams', '$location', function($scope, $routeParams, $location)  {
	 
	$scope.selectedHashtag = $routeParams.selectedHashtag;
	$scope.usage = 'daily';

	$scope.updateGrapgh = function(selectedHT) {

		document.getElementById('clustering-container').innerHTML = '';
		sigma.parsers.json('/api/clusterData' + (selectedHT ? '/' + selectedHT : '') , {
			container: 'clustering-container',
			settings: {
			  defaultNodeColor: '#ec5148',
			  labelThreshold: 1000000,
			  minEdgeSize: 3,
			  maxEdgeSize: 18
			}
		  });
	}

	$scope.hashtagSelected = function(ht) {
	  $scope.selectedHashtag = ht;
	  $location.path('/clustering/' + (ht || ''), false);
	  $scope.updateGrapgh($scope.selectedHashtag);
	}

	$scope.setUsage = function(newVal) {
	  $scope.usage = newVal;
	}
	
	$scope.updateGrapgh($scope.selectedHashtag);
}]);