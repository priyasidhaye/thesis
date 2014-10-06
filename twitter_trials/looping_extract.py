import extract_tweets_utils as utils
from datetime import datetime
import time

flag = 1
while (flag) :
	print 'Back up' 
	now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  
	utils.write_tweets_to_file(utils.get_tweets_for_trends(utils.get_current_trends()), './data/tweets/' + now)
	print 'Sleeping'
	time.sleep(900)	
