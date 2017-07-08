htViewerApp.controller('HashtagSelectionController', function($scope, $location) {
        
    var pools = {
    	tweets: 'tweets',
    	hashtags: 'hashtags'
    };
    var tweetsBy = {
    	author: 'author',
    	date: 'date'

    };
    var hashtagsBy = {
    	popularity: 'popularity',
    	text: 'text'
    };

	$scope.fromPool = pools.tweets;
	$scope.tweetsBy = tweetsBy.author;
	$scope.hashtagsBy = hashtagsBy.popularity;

	$scope.$watch('hashtagsBy', function() {
        
        if ($scope.hashtagsBy === hashtagsBy.popularity) {
        	getMostPopularHashtags();
        }
    });

    $scope.$watch('tweetsBy', function() {
        
        if ($scope.authors == null) {
        	$.ajax({
        		method: 'GET',
        		url: '/api/authors'
        	})
        	.done(function (data) {
        		$scope.authors = JSON.parse(data).authors;
        	});
        }
    });

    $scope.getTweetsByAuthor = function (author) {
    	$scope.selectedAuthor = author;
    	
    	$.ajax({
    		method: 'GET',
    		url: '/api/tweet/' + author
    	})
    	.done(function (data) {
    		$scope.tweets = JSON.parse(data).tweets.slice(0, 100); // show only first 100 tweets
            console.log($scope.tweets[2][3]);
    		$scope.$digest();
    	});
    }

    $scope.getHashtagsByTweet = function(tweetId) {
        $scope.selectedTweet = tweetId;
    	$.ajax({
    		method: 'GET',
    		url: '/api/hashtagsByTweet/' + tweetId
    	})
    	.done(function (data) {
    		$scope.hashtags = JSON.parse(data).hashtags;
    		$scope.$digest();
    	});
    }

    function getMostPopularHashtags() {
    	// get most popular, export to $scope.hashtags...
    }
});