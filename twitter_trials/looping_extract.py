import extract_tweets_utils as utils

flag = 1
while (flag) : 
	utils.write_tweets_to_file(utils.get_tweets_for_trends(), 'timestamp')
	#sleep_till_reset
