import extraction_utils
import data_utils
import sys
import time
import simplejson as json


input_filename = sys.argv[1] + 'input.txt'
run_number = 0

output_filename = sys.argv[1] + 'output' + str(run_number) + '.json'
#get list of hashtags/terms to search data for
tweetsets = {}
with open(input_filename, 'r') as search_term_file : 
	for search_term in search_term_file :
		#Call function to return and write to file list of tweets
		tweetsets[search_term] =  extraction_utils.search_for_term(search_term, 10000)
		print("Extracted data for : " + search_term)
		time.sleep(300)
		
#Write all tweets extracted to a file
data_utils.write_tweets_to_file(tweetsets, sys.argv[1] + 'temp/all_tweets.json')
'''
with open(sys.argv[1]  + 'temp/all_tweets.json', 'w') as output_file_object : 
	output_file_object.write(json.dumps(tweetsets))
'''	
#Go through all the tweets and extract links and write tweet id -> link json
#Go through all the links and extract articles



