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
	
#Write search of a specific term and return tweets in a list
def search_for_term (search_term, max_no = 1000) :
	search_result = api.GetSearch(term = search_term, lang = 'en', count = max_no, include_entities = 'true')
	tweets = {}
	for tweet in search_result :
			tweets[tweet.id] = tweet
	return tweets
