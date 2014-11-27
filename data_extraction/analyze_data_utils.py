import simplejson as json
import matplotlib.pyplot as plt
import newspaper
from newspaper import Article

#Returns the numbero of unique users
def number_of_unique_users(filename) :
	with open(filename, 'r') as data_obj :
		data = json.load(data_obj) 
		unique_users = []
		for search_term in data : 
			tweets = data[search_term]
			for tweet_id in tweets :
				tweet = tweets[tweet_id]
				if tweet['user']['id'] not in unique_users :
					unique_users.append(tweet['user']['id'])
	return len(unique_users)
				
#Currently returns number of tweets and tweets with urls in it.
def get_numbers_on_file(filename) :
	with open(filename, 'r') as data_obj : 
		data = json.load(data_obj)
		count_of_tweets = 0
		count_of_tweets_with_links = 0
		for search_term in data : 
			tweets = data[search_term]
			count_of_tweets += len(tweets.keys())
			for tweet_id in tweets.keys() :
				tweet = tweets[tweet_id]
				if 'urls' in tweet.keys() :
					count_of_tweets_with_links += 1
	return [count_of_tweets, count_of_tweets_with_links]

#Currently, returns the nummber of times a hashtag has been used and the number of unique hashtags
def hashtag_numbers(filename) :
	with open(filename, 'r') as data_obj :
		data = json.load(data_obj)
		hashtags = {}
		for search_term in data :
			tweets = data[search_term]
			for tweet_id in tweets :
				tweet = tweets[tweet_id]
				if 'hashtags' in tweet.keys() :
					for hashtag in tweet['hashtags'] :
						if hashtag in hashtags.keys() :
							hashtags[hashtag] += 1
						else :						
							hashtags[hashtag] = 1
		plt.bar(range(len(hashtags)), hashtags.values(), align='center')
		plt.xticks(range(len(hashtags)), hashtags.keys())
		plt.show()

	return len(hashtags.keys())

#writes all unique urls to a file?
def url_experiments (filename, op_file) :
	url_dict = {}
	with open(filename, 'r') as data_obj :
		data = json.load(data_obj)
		for search_term in data :
			tweets = data[search_term]
			for tweet_id in tweets :
				if 'urls' in tweets[tweet_id] :
					for t_url in tweets[tweet_id]['urls'] :
						  url_dict[tweet_id] = tweets[tweet_id]['urls'][t_url]
	with open(op_file, 'w') as op_fileobj :
		op_fileobj.write(json.dumps(url_dict))
			
	return

def url_flip (filename, op_file) :
	url_flipped = {}
	with open(filename, 'r') as data_obj :
		data = json.load(data_obj)
		for tweet_id, url in data.items() :
			if url not in url_flipped.keys() : 
				url_flipped[url] = [tweet_id]
			else :
				url_flipped[url].append(tweet_id)
	print len(url_flipped.keys())
	with open(op_file, 'w') as flip_url :
		flip_url.write(json.dumps(url_flipped))
	return

#Fetches the actual text of the urls. 
#First trial run to see how many come up with decent texts
def fetch_url_data(filename, op_file, bad_urls) :
	urls = {}
	new_urls = {}
	with open(filename, 'r') as url_file : 
		urls = json.load(url_file)
	for url in urls :
		try : 
			article = Article(url, 'en')
			article.download()
			article.parse()
		except :
			with open(bad_urls, 'a') as bad_urls_obj :
				bad_urls_obj.write(url +'\n')
			continue
		new_id = generate_id(url)
		temp = {}
		temp['url'] = url
		temp['title'] = article.title
		temp['text'] = article.text
		temp['tweets'] = urls[url]
		print article.title
		new_urls[new_id] = temp
	with open(op_file,'w') as output_file :
		output_file.write(json.dumps(new_urls))

def generate_id(url):
	generate_id.url_id_count += 1
	return generate_id.url_id_count
generate_id.url_id_count = 0
