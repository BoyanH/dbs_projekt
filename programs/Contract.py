class Contract:

	CSV_INITIAL = 'american-election-tweets.csv'
	CSV_CLEAN = 'data-cleaned.csv'

	TABLE_WEEK = 'week'
	TABLE_DAY = 'day'
	TABLE_TWEET = 'tweet'
	TABLE_HASHTAG = 'hashtag'
	TABLE_USED_IN = 'usedin'
	TABLE_USED_ON = 'usedon'
	TABLE_IS_IN = 'isin'
	TABLE_POSTED_IN = 'postedin'
	TABLE_USED_TOGETHER_WITH = 'usedtogetherwith'
	TABLE_CONTAINS = 'contains'
	TABLE_REPRESENTATION_EDGE = 'representationedge'
	TABLE_CLUSTER = 'cluster'

	ADD_TO_TABLE_KEY = 'addToTable'

	COUNT_COLUMN = 'count'
	ID_COLUMN = 'id'
	TWEET_ID_COLUMN = 'tweetid'
	AUTHOR_COLUMN = 'author'
	TEXT_COLUMN = 'text'
	DATE_COLUMN = 'date'
	START_DATE_COLUMN = 'startdate'
	END_DATE_COLUMN = 'enddate'
	WEEK_START_DATE_COLUMN = 'weekstartdate'
	DAY_DATE_COLUMN = 'daydate'
	TIME_COLUMN = 'time'
	RATING_COLUMN = 'rating'
	PRIMARY_HASHTAG_COLUMN = 'primaryhashtag'
	TOGETHER_WITH_HASHTAG_COLUMN = 'togetherwithhashtag'
	TEXT_LOWER_CASE_COLUMN = 'textlowercase'
	HASHTAG_TEXT_COLUMN = 'hashtagtext'
	HASHTAG1_COLUMN = 'hashtag1'
	HASHTAG2_COLUMN = 'hashtag2'
	EDGE_WIDTH_COLUMN = 'edgewidth'
	BELONGS_TO_CLUSTER_ID = 'belongstoclusterid'
	CENTER_COORDINATES = 'centercoordinates'
	COORDINATES_COLUMN = 'coordinates'

	TEXT_ENTRY = TEXT_COLUMN
	HANDLE_ENTRY = 'handle'
	
	IGNORE_DUPLICATES_IN_TABLES = [TABLE_WEEK],

	USED_TOGHETHER_WITHS = 'usedTogetherWiths'