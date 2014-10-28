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
	for tweet in tweets : 
		tweet_dict[tweet.id] = tweet.AsDict()
	print 'Printing tweets'
	with open(filename, 'w') as op_file :
		op_file.write(json.dumps(tweet_dict))
	return


#Returns list of trend names only and write to file if filename
def get_current_trends() :
	trends = api.GetTrendsCurrent()
	trends_names = [trend.name for trend in trends]
	print 'Printing trends'
	with open('./data/trends/' + trends[0].timestamp, 'w') as op_file :		
		op_file.write(json.dumps(trends_names))
	return trends_names


#Returns list of tweets for a given list of trends
def get_tweets_for_trends(trends, count_per_trend = 100) :
	tweets = []
	for trend_name in trends :
		search_result = api.GetSearch(term = trend_name, lang = 'en', count = count_per_trend, include_entities = 'true') 
		for tweet in search_result :
			tweets.append(tweet) 
	return tweets		

#Writes all the unique tweets from files in the given directory path to the given file. 
#If removeRT = 1, removes Retweet ids from the file.
def write_all_tweets_to_file(dir_path, file_path,removeRT) :
	from os import listdir
	from os.path import join
	
	with open(file_path, 'w') as op_file_object : 
		files = [f for f in listdir(dir_path)]
		unique_ids = []
		for file_name in files : 
			print file_name
			with open(join(dir_path, file_name), 'r') as tweet_file_object :
				json_object = json.load(tweet_file_object)
				keys_in_file = json_object.keys()
				for key in keys_in_file :
					if removeRT is 1 and "RT" in key :
						continue
					if key not in unique_ids : 
						op_file_object.write(json_object[key]["text"].encode('utf-8'))
						op_file_object.write("\n\n")
						unique_ids.append(key)
	return	
	
#Write search of a specific hashtag to file
def search_and_write(search_term, file_name) :
	search_result = api.GetSearch(term = search_term, lang = 'en', count = 2000, include_entities = 'true')
	tweets = []
	for tweet in search_result :
			tweets.append(tweet) 
	write_tweets_to_file(tweets, file_name)
	return


#For every tweet execute function given in parameter
def for_every_tweet(filename, op_file_name, function_name) :
	op_dict = {}
	with open(filename,'r') as file_obj : 
		tweets = json.load(file_obj)
		for tweet_id in tweets :
		 	return_value = function_name(tweets[tweet_id])
			if return_value != "" :
				op_dict[tweet_id] = return_value
	with open(op_file_name, 'w') as op_file_obj :
		op_file_obj.write(json.dumps(op_dict))
	return

#Return links if links are present in a tweet, null if no url.
def return_urls(tweet) :
	ret_string = ""
	if u'urls' in tweet.keys() :
		for url in tweet['urls'] :
			ret_string += url + '\n'	
	return ret_string
	return
