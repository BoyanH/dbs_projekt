class Contract:

	TABLE_WEEK = 'week'
	TABLE_TWEET = 'tweet'
	TABLE_HASHTAG = 'hashtag'
	TABLE_USED_IN = 'usedin'
	TABLE_POSTED_IN = 'postedin'
	TABLE_USED_TOGETHER_WITH = 'usedtogetherwith'
	TABLE_CONTAINS = 'contains'

	ADD_TO_TABLE_KEY = 'addToTable'

	COUNT_COLUMN = 'count'
	ID_COLUMN = 'id'
	TWEET_ID_COLUMN = 'tweetid'
	AUTHOR_COLUMN = 'author'
	TEXT_COLUMN = 'text'
	START_DATE_COLUMN = 'startdate'
	END_DATE_COLUMN = 'enddate'
	WEEK_START_DATE_COLUMN = 'weekstartdate'
	TIME_COLUMN = 'time'
	RATING_COLUMN = 'rating'
	PRIMARY_HASHTAG_COLUMN = 'primaryhashtag'
	TOGETHER_WITH_HASHTAG_COLUMN = 'togetherwithhashtag'
	TEXT_LOWER_CASE_COLUMN = 'textlowercase'
	HASHTAG_TEXT_COLUMN = 'hashtagtext'

	TEXT_ENTRY = TEXT_COLUMN
	HANDLE_ENTRY = 'handle'
	
	IGNORE_DUPLICATES_IN_TABLES = [TABLE_WEEK]