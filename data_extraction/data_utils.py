import simplejson as json
import twitter
#This file handles everything to do with saving/accessing data.
#All write functions write objects to json files
#All read functions read json object and return objects.

#writes list of tweet objects to the given file as a JSON string
def write_tweets_to_file (tweetsets, filename) :
	for search_term in tweetsets.keys() :
		tweets = tweetsets[search_term]
		tweet_dict = {}
		for tweet_id in tweets.keys() :
			tweet_dict[tweet_id] = tweets[tweet_id].AsDict()
		tweetsets[search_term] = tweet_dict		
	print 'Printing tweets'
	with open(filename, 'w') as op_file :
		op_file.write(json.dumps(tweetsets))
	return

