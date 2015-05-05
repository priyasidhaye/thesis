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

#Writes a display-ready json file in folder
def write_tweets_for_display(input_file, filename) : 
    tweetsets = {}
    with open(input_file, 'r') as data_file :
        tweetsets = json.load(data_file)
    tweetset_disp= {}
    for search_term in tweetsets.keys() :
        tweets = tweetsets[search_term]
        tweet_dict = {}
        for tweet_id in tweets.keys() :
            tweet = tweets[tweet_id]
            tweet_disp = {}
            tweet_disp['text'] = tweet['text']
            tweet_disp['created_at'] = tweet['created_at']
            if 'hashtags' in tweet.keys() :
                tweet_disp['hashtags'] = tweet['hashtags']
            if 'retweeted' in tweet.keys() :
                tweet_disp['retweeted'] = tweet['retweeted']
            if 'urls' in tweet.keys() :
                tweet_disp['urls'] = tweet['urls']
            if 'retweet_count' in tweet.keys() :
                tweet_disp['retweet_count'] = tweet['retweet_count']
            tweet_dict[tweet_id] = tweet_disp
        tweetset_disp[search_term] = tweet_dict
    with open(filename, 'w') as op_file :
        op_file.write(json.dumps(tweetset_disp))
    return

#Add only unique tweets to a total data file
def append_unique_tweets_data(input_file, data_file) : 
    #build hash of ids in one search term.
    with open(data_file, 'r') as data :
        all_data = json.load(data)
        with open(input_file, 'r') as input_fileobj :
            current_data = json.load(input_fileobj)
            for search_term in current_data.keys() :
                if search_term in all_data.keys() :
                    #check for non-repeating ids and append
                    all_data[search_term] = append_unique_tweets(all_data[search_term], current_data[search_term])
                else :
                    all_data[search_term] = current_data[search_term]
    with open(data_file, 'w') as op :
        op.write(json.dumps(all_data))
    return

#Helper method
def append_unique_tweets(compare_data, current_data) : 
    for tweet_id in current_data.keys() :
        if not(tweet_id in compare_data.keys()) :
            compare_data[tweet_id] = current_data[tweet_id]
    return compare_data
