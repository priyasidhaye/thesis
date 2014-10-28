import extract_tweets_utils
#These are for resolving path names. Will be refactored and moved to a package.
import httplib
import urlparse
import socket
import simplejson as json
#These are for getting newspaper text. Will be refactored
import newspaper
from newspaper import Article
extract_tweets_utils.search_and_write('#mangalayan', './data_individual_terms/mangalayan/results.json')

extract_tweets_utils.for_every_tweet('./data_individual_terms/mangalayan/results.json', './data_individual_terms/mangalayan/urls.txt', extract_tweets_utils.return_urls) 
'''
#Code for resolving urls. Will be refactored.
with open('./data_individual_terms/ebola/ebola_urls.txt','r') as file_handle : 
	with open('./data_individual_terms/ebola/resolved_urls.txt','w') as op_file_handle :

		for url in file_handle: 
			parts = urlparse.urlparse(url)
			conn = httplib.HTTPConnection(parts.netloc.strip())
			conn.request("HEAD", parts.path.strip())	
			response = conn.getresponse()
			url2 = response.getheader("Location")
			print "initial: " + url2
			#op_file_handle.write(response.getheader("Location") + "\n")
			conn.close()
			#Go through same steps again while link is shortened
			while response.status == 301 :
				parts = urlparse.urlparse(url2)
				conn = httplib.HTTPConnection(parts.netloc)
				conn.request("HEAD", parts.path)	
				response = conn.getresponse()
				if response.status == 301 :
					url2 = response.getheader("Location")
					print "next ones: " + url2
					conn.close()
			op_file_handle.write(url2 + "\n")

'''

#For getting and writing body of links. Will be refactored.
#using count for now, has to be modified to tweet-id
with open('./data_individual_terms/mangalayan/urls.txt','r') as file_handle : 
	json_object = json.load(file_handle)
	for key in json_object: 
		article = Article(json_object[key], 'en')
		article.download()
		article.parse()
		with open('./data_individual_terms/mangalayan/contents/' + key ,'w') as text_file : 
			text_file.write((article.text).encode("utf-8"))
		print article.title
