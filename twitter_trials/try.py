import simplejson
import twitter
import oauth2 as oauth
import simplejson as json

#Reading from file
with open('.config','r') as config_file :
		json_obj = json.loads(config_file.readline())
		api = twitter.Api(
			consumer_key = json_obj["consumer_key"],
			consumer_secret = json_obj["consumer_secret"],
			access_token_key = json_obj["access_token_key"],
			access_token_secret = json_obj["access_token_secret"]
		) 

#Actual request and print to terminal
search = api.GetSearch(term='#harrypotter', lang='en', result_type='recent', count=100, max_id='') 
for t in search:
	print t.user.screen_name
	print t.text.encode('utf-8')

