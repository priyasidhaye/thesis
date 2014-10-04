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

def get_status_by_id (id) : 
	return api.GetStatus(id)

def write_tweets_to_file (tweets, filename) :
	tweet_dict = {}
	counter = 0
	for tweet in tweets : 
		tweet_dict[tweet.id] = tweet.AsDict()

	with open(filename, 'w') as op_file :
		op_file.write(json.dumps(tweet_dict))		
				
