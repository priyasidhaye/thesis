import simplejson
import twitter
import oauth2 as oauth

#Reading from file
with open('.config','r') as config_file :
		api = twitter.Api(
			consumer_key = config_file.readline().strip(),
			consumer_secret = config_file.readline().strip(),
			access_token_key = config_file.readline().strip(),
			access_token_secret = config_file.readline().strip()
			) 

search = api.GetSearch(term='#freecoffee', lang='en', result_type='recent', count=100, max_id='') 
for t in search:
	print t.user.screen_name
	print t.text.encode('utf-8')
	print 



