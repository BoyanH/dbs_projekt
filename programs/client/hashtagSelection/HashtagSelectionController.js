htViewerApp.controller('HashtagSelectionController', function($scope, $location, $rootScope) {
        
    var pools = {
    	tweets: 'tweets',
    	hashtags: 'hashtags',
        allHashtags: 'allHashtags'
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

	$scope.setPool =  function(pool) {
        $scope.fromPool = pool;
        if (pool === pools.tweets) {
        	$scope.setTweetBy($scope.tweetsBy);
        } else if (pool === pools.hashtags){
            $scope.setHashtagsBy($scope.hashtagsBy);
        } else {
            $scope.selectHashtag(null);
        }
    };

    $scope.setTweetBy = function(newVal) {
        $scope.tweetsBy = newVal;
        if ($scope.authors == null) {
        	$.ajax({
        		method: 'GET',
        		url: '/api/authors'
        	})
        	.done(function (data) {
        		$scope.authors = JSON.parse(data).authors;
                $scope.$digest();
        	});
        } else if ($scope.selectedAuthor != null && newVal == tweetsBy.author) {
            $scope.getTweetsByAuthor($scope.selectedAuthor);
        } else if ($scope.selectedDates != null && newVal == tweetsBy.date) {
            $scope.getTweetsByDates();
        }
    };

    $scope.setHashtagsBy = function(newVal) {
        $scope.hashtagsBy = newVal;

        if (newVal == hashtagsBy.popularity || !newVal) {
            getMostPopularHashtags();
        } else if($scope.searchWord != null) {
            $scope.getHashtagsBySearch($scope.searchWord);
        }
    }

    $scope.getTweetsByAuthor = function (author) {
    	$scope.selectedAuthor = author;
    	
    	$.ajax({
    		method: 'GET',
    		url: '/api/tweet/' + author
    	})
    	.done(function (data) {
    		$scope.tweets = JSON.parse(data).tweets.slice(0, 100); // show only first 100 tweets
    		$scope.$digest();
    	});

        if ($scope.selectedTweet) {
            $scope.getHashtagsByTweet($scope.selectedTweet);
        }
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

    $scope.getHashtagsBySearch = function(word) {
        $.ajax({
            method: 'GET',
            url: '/api/searchHashtags/' + word
        })
        .done(function (data) {
            $scope.hashtags = JSON.parse(data).hashtags.slice(0, 30);
            $scope.$digest();
        });
    }

    $scope.selectHashtag = function(hashtag) {
        $scope.selectedHashtag = hashtag;
        $scope.$parent.hashtagSelected(hashtag);
    }

    function getMostPopularHashtags() {
        $.ajax({
            method: 'GET',
            url: '/api/getTopHashtags'
        })
        .done(function (data) {
            $scope.hashtags = JSON.parse(data).hashtags.slice(0, 30);
            $scope.$digest();
        });
    }

    $scope.setPool($scope.fromPool);
});