htViewerApp.controller('ClusteringController', function($scope) {
     
     updateGrapgh();

});

function updateGrapgh() {
	sigma.parsers.json('/api/clusterData', {
        container: 'container',
        settings: {
          defaultNodeColor: '#ec5148',
          labelThreshold: 1000000,
          minEdgeSize: 3,
          maxEdgeSize: 18
        }
      });
}