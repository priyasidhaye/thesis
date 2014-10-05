import twitter
import oauth2 as oauth
import simplejson as json

#Create api object using tokens from .config file
with open('.config','r') as config_file :
	json_obj = json.loads(config_file.readline())
	api = twitter.Api(
		consumer_key = json_obj["consumer_key"],
		consumer_secret = json_obj["consumer_secret"],
		access_token_key = json_obj["access_token_key"],
		access_token_secret = json_obj["access_token_secret"]
	)

#Returns list of tweet objects for list of ids
def get_status_by_ids (ids) : 
	return [api.GetStatus(id) for id in ids]

#writes list of tweet objects to the given file as a JSON string
def write_tweets_to_file (tweets, filename) :
	tweet_dict = {}
	counter = 0
	for tweet in tweets : 
		tweet_dict[tweet.id] = tweet.AsDict()

	with open(filename, 'w') as op_file :
		op_file.write(json.dumps(tweet_dict))		
				
	return


#Returns list of trend names only
def get_current_trends() :
	return [trend.name for trend in api.GetTrendsCurrent()]


#Returns list of tweets for a given list of list of trends
def get_tweets_for_trends(trends = get_current_trends(), count_per_trend = 100) :
	return [api.GetSearch(term = trend_name, lang = 'en', count = count_per_thread, include_entities = 'true') for trend_name in trends]
		
