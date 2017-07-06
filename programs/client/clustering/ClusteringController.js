htViewerApp.controller('ClusteringController', function($scope) {
     
     updateGrapgh();   
	// $.ajax({
	// 	method: 'GET',
	// 	url: '/api/cluster.json'
	// }).done(function (json) {
	// 	console.log(json);
	// 	updateGrapgh(json);
	// })

});

function updateGrapgh() {
	sigma.parsers.json('/api/clusterData', {
        container: 'container',
        settings: {
          defaultNodeColor: '#ec5148'
        }
      });
}