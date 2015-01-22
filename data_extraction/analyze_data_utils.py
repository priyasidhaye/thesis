import simplejson as json
import matplotlib.pyplot as plt
import newspaper
from newspaper import Article
from boilerpipe.extract import Extractor
import urlparse
import httplib
import nltk
from urllib import urlopen
import sklearn.metrics as metrics
import skll

#Returns the number of unique users
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
def fetch_url_data(filename, op_file, bad_urls, csv_file) :
	urls = {}
	new_urls = {}
	with open(filename, 'r') as url_file : 
		urls = json.load(url_file)
	
	with open(csv_file, 'w') as csv_file_obj :
		csv_file_obj.write("ID,URL,Text1,Text2,Tags,Comments,T1orT2\n")
	for url in urls :
		try : 
			article = Article(url, 'en')
			article.download()
			article.parse()

			extractor = Extractor(extractor='ArticleExtractor', url=url)
			extracted_text = extractor.getText()
			extracted_html = extractor.getHTML()

		except :
			with open(bad_urls, 'a') as bad_urls_obj :
				bad_urls_obj.write(url +'\n')
			continue
		new_id = generate_id(url)
		temp = {}
		temp['url'] = url
		temp['title'] = article.title
		temp['text_newspaper'] = article.text
		temp['text_boilerpipe'] = extracted_text
		temp['html'] = extracted_html
		temp['tweets'] = urls[url]
		print article.title
		new_urls[new_id] = temp
		with open(csv_file, 'a') as csv_file_obj : 
			line = str(new_id) + ',' + url + ',"' + article.text + '","' + extracted_text + '",,,,\n'
			csv_file_obj.write(line.encode('utf-8'))

	with open(op_file,'w') as output_file :
		output_file.write(json.dumps(new_urls))

def generate_id(url):
	generate_id.url_id_count += 1
	return generate_id.url_id_count
generate_id.url_id_count = 0


def calculate_agreement(file1, file2, disagree_urls) :
	with open(file1, 'r') as file_obj1 :
		data1 = json.load(file_obj1)
	with open(file2, 'r') as file_obj2 :
		data2 = json.load(file_obj2)
	agreement = {'traditional' : 0, 'nontraditional' : 0, 'mixed' : 0, 'descriptive' : 0, 'evaluative' : 0}
	non_agreement =	 {'traditional' : 0, 'nontraditional' : 0, 'mixed' : 0, 'descriptive' : 0, 'evaluative' : 0}
	tag_check = ['traditional', 'nontraditional']
	tag_dict = {'traditional' : 1, 'nontraditional' : 2, 'mixed' : 3, 'descriptive' : 4, 'evaluative' : 3}
	agree_consider = 0
	agree_all = 0
	agree_1 = 0
	agree_none = 0
	agree_consider_yes = 0
	tags1_s = []
	tags1_c = []
	tags2_s = []
	tags2_c = []
	tags1k = []
	tags2k = []
	with open(disagree_urls, 'w') as write_obj :
		write_obj.write('URL'+'\t'+ 'File1 source' +'\t'+ 'File2  source' +'\t'+ 'File1 intent' +'\t' + 'File2 intent' +'\n')

	for url_id in data1 :
		if data1[url_id]['consider'] == data2[url_id]['consider'] :
			agree_consider += 1
			if data2[url_id]['consider']  == 'y' :
				agree_consider_yes += 1
				agree_tags = 0
				for tag in data2[url_id]['tags'] :
					if tag in data1[url_id]['tags'] :
						agree_tags += 1
						agreement[tag] += 1

				if agree_tags == 2 :
					agree_all += 1
				elif agree_tags == 1 :
					agree_1 += 1
					with open(disagree_urls, 'a') as write_obj :
						write_obj.write(data1[url_id]['url'] + '\t' + data1[url_id]['tags'][0].encode('utf-8') + '\t' + data2[url_id]['tags'][0].encode('utf-8') + '\t' + data1[url_id]['tags'][1].encode('utf-8') + '\t' + data2[url_id]['tags'][1].encode('utf-8') +'\n')
				else :
					agree_none += 1
					with open(disagree_urls, 'a') as write_obj :
						write_obj.write(data1[url_id]['url'] + '\t' + data1[url_id]['tags'][0].encode('utf-8') + '\t' + data2[url_id]['tags'][0].encode('utf-8') + '\t' + data1[url_id]['tags'][1].encode('utf-8') + '\t' + data2[url_id]['tags'][1].encode('utf-8') +'\n')

				for tag in data1[url_id]['tags'] :
					non_agreement[tag] += 1
					if tag in tag_check :
						tags1_s.append(tag)
					else :
						tags1_c.append(tag)
					tags1k.append(tag_dict[tag])
				for tag in data2[url_id]['tags'] :
					non_agreement[tag] -= 1
					if tag in tag_check :
						tags2_s.append(tag)
					else :
						tags2_c.append(tag)
					tags2k.append(tag_dict[tag])


	print agree_consider_yes
	print 'agreement on consider url : ', float(agree_consider) / float(len(data1.keys())) * 100
	print 'Agreement on all tags : ' ,(float(agree_all) / float(agree_consider_yes) * 100)
	print 'Agreement on one tag : ' , (float(agree_1) / float(agree_consider_yes) * 100)
	print 'Agreement on no tag : ' , (float(agree_none) / float(agree_consider_yes) * 100)
	print 'Tag-wise agreement : '
	for tag in agreement :
		print tag,' : ', agreement[tag]
		print non_agreement[tag]
		

		
	print metrics.confusion_matrix(tags1_s,tags2_s)
	print metrics.confusion_matrix(tags1_c,tags2_c)
	print skll.metrics.kappa(tags1k,tags2k)
	t1 = [tag_dict[x] for x in tags1_s]
	t2 = [tag_dict[x] for x in tags2_s]
	print 'Source kappa ' ,skll.metrics.kappa(t1,t2)
	t1 = [tag_dict[x] for x in tags1_c]
	t2 = [tag_dict[x] for x in tags2_c]
	print 'Intent kappa ' ,skll.metrics.kappa(t1,t2)
'''
def view_diagree_urls (tagged1, tagged2, write_urls) :
	with open(tagged1, 'r') as t1 :
		data1 = json.load(t1)
	with open(tagged2, 'r') as t2 :
		data2 = json.load(t2)
	with open(write_urls, 'w') ad write_obj :
		for url_id in data1 :
			if data1[url_id]['consider'] == data2[url_id]['consider'] and data1[url_id]['consider'] == 'y' :
				if
				'''
