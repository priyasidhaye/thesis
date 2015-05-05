import simplejson as json
import numpy as np
from nltk.corpus import stopwords
import data_structures
import sys
import numpy as np
import matplotlib.pyplot as plt


def distribute_over_hashtags(tweet_file, url_details_file, counts_file) :
    with open(tweet_file, 'r') as tweets_obj:
        tweets_data = json.load(tweets_obj)

    with open(url_details_file, 'r') as url_obj:
        urls_data = json.load(url_obj)

    weights = {}
    with open(counts_file, 'r') as counts_obj:
        for line in counts_obj:
            parts = line.split(',')
            weights[str(parts[0])] = parts[1]

    print weights
    for hashtag in tweets_data :
        counts = []
        number_of_articles = 0
        print hashtag
        for tweet_id in tweets_data[hashtag]:
            if 'urls' in tweets_data[hashtag][tweet_id].keys():
                for url in tweets_data[hashtag][tweet_id]['urls']:
                    #Look for url in urls_data
                    for url_id in urls_data:
                        if tweets_data[hashtag][tweet_id]['urls'][url] == urls_data[url_id]['url']:
                            if url_id in weights.keys():
                                print weights[url_id]
                                number_of_articles += 1
                                counts.append(float(weights[url_id]))


        with open('formality_over_hashtags.csv','a') as op_obj:
            if len(counts) != 0:
                op_obj.write(hashtag.strip()+','+str(np.mean(counts))+','+str(np.std(counts))+','+str(number_of_articles)+','+str(len(tweets_data[hashtag].keys()))+'\n')

            else:
                op_obj.write(hashtag.strip()+',0,0\n')


def find_pos_tweets(tweet_file, url_details_file, text_file):
    with open(tweet_file, 'r') as tweets_obj:
        tweets_data = json.load(tweets_obj)

    with open(url_details_file, 'r') as url_obj:
        urls_data = json.load(url_obj)

    with open(text_file, 'r') as text_obj:
        text_data = json.load(text_obj)

    count = 0

    for hashtag in tweets_data:
        with open("log.txt", 'a') as log_obj:
            log_obj.write(hashtag)
        for tweet_id in tweets_data[hashtag]:
            if 'urls' in tweets_data[hashtag][tweet_id].keys():
                for url in tweets_data[hashtag][tweet_id]['urls']:
                    urlid = get_urlid(urls_data, text_data, tweets_data[hashtag][tweet_id]['urls'][url])
                    if urlid != 0:

                        text = text_data[urlid]['text']
                        '''
                        pos,title = get_tweet_posn(tweets_data[hashtag][tweet_id]['text'], text,text_data[urlid]['title'])
                        with open('positions.csv', 'a') as pos_obj:
                            pos_obj.write(str(tweet_id) + ',' + str(urlid) + ',' + str(pos) + ',' + str(len(text)) + ',' + title +'\n')

                        p_match = cal_percentage_match (tweets_data[hashtag][tweet_id]['text'],  text)
                        with open('percentmatch.csv', 'a') as p_obj:
                            p_obj.write(str(tweet_id)+ ',' + str(urlid) + ',' + str(p_match) + '\n')

                        max_sent, total_sentences, max_match = cal_percent_tweet_window_article(tweets_data[hashtag][tweet_id]['text'], urlid)
                        if max_match == 0:
                            continue
                        if count < 5 :
                            print tweets_data[hashtag][tweet_id]['text']
                            print text
                            print max_sent, " ", max_match
                            count += 1
                        with open('matchwindow.csv', 'a') as p_obj:
                            p_obj.write('\n' + str(tweet_id) + ',' + str(urlid) + ',' + str(max_sent) + ',' + str(total_sentences) + ',' +str(max_match))
                        '''

                        lcs = lcs_length(tweets_data[hashtag][tweet_id]['text'], text)
                        with open('lcs.csv','a') as lcs_obj:
                            lcs_obj.write(str(tweet_id)+ ',' + str(urlid) + ',' + str(lcs) + '\n')


def get_urlid(data, data2, url):
    for urlid in data:
        if data[urlid]['url'] == url and urlid in data2.keys():
            return urlid
    return 0

def get_tweet_posn(tweet, text, title):
    tweet_text = get_tweet_text(tweet)
    title = 'n'
    if title == tweet_text:
        title = 'y'
    pos = text.find(tweet_text)
    if pos != -1:
        with open('tweet_text.txt', 'a') as a_obj:
            a_obj.write('Tweet : ' + tweet.encode('utf-8') + '\n' + 'Title : ' + title.encode('utf-8') + '\n' + 'Text : \n' + text.encode('utf-8') + '\n\n\n')
    return text.find(tweet_text),title

def get_tweet_text(tweet):
    temp = [word for word in tweet.split() if '@' not in word and '#' not in word and 'http' not in word and word != 'RT']
    return ' '.join(temp)


def remove_stop_words(text):
    stop = stopwords.words('english')
    words = text.split()
    remains = [word for word in words if word not in stop]
    return ' '.join(remains)


def cal_percentage_match(tweet, text):
    tweet_words = remove_stop_words(tweet)
    text_words = remove_stop_words(text)
    matches = [1 for word in tweet_words if word in text_words]
    percent = float(len(matches)) / float(len(tweet_words)) * 100
    return percent

# Make changes so that if text of tweets are same, article gets considered only once.
def cal_percent_tweet_window_article(tweet, article_id):
    # Handle exception file not in folder
    with open("log.txt", 'a') as log_obj:
        log_obj.write("Processing " + article_id + "\n")
    file_path = "../data/op/" + article_id.encode('utf-8') + '.xml'
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        with open("log.txt", 'a') as log_obj:
            log_obj.write(article_id + "Not found" + "\n")
        return 0, 0, 0

    document = data_structures.read_corenlp_doc(file_path, int(article_id))

    # Put all sentences together
    sentences = {}
    for sent_id in document.sents:
        sentence = document.sents[sent_id]
        tokens_list = list()
        for tok_id in sentence.tokens:
            tokens_list.append(sentence.tokens[tok_id].word)
        sentences[sent_id] = ' '.join(tokens_list)

    match_scores = {}
    # Assuming context window = 3 sentences.
    # Generalize this to any window size
    if len(sentences) > 2:
        max_value = 0
        max_sent = 0
        for i in range(1, len(sentences) - 2):
            txt = sentences[i] + ' ' + sentences[i+1] + ' ' + sentences[i+2]
            temp_value = cal_percentage_match(tweet, txt)
            match_scores[i] = temp_value
            if temp_value > max_value:
                max_value = temp_value
                max_sent = i
        try:
            # print max(match_scores.values(), key=match_scores.get), " ", len(sentences)
            return max_sent, len(sentences), max_value
        except ValueError:
            with open("log.txt", 'a') as log_obj:
                log_obj.write(article_id + "No results" + "\n")
            return 0, 0, 0

    else:
        if len(sentences) == 1:
            txt = sentences[1]
        else:
            txt = sentences[1] + ' ' + sentences[2]
        return 1, len(sentences), cal_percentage_match(tweet, txt)


# This is specifically for the match file written for sentence-window matches.
def make_unique_urls(tweet_file, match_file, match_file_new):
    # Make a dictionary that goes from tweet-id to tweet-text
    with open(tweet_file, 'r') as tweet_obj:
        data = json.load(tweet_obj)

    tweet_dict = {}
    for hashtag in data:
        for tweet_id in data[hashtag]:
            try:
                tweet_dict[str(tweet_id)] = data[hashtag][tweet_id]['text']
                with open('tweetids.txt','a') as t_obj:
                    t_obj.write(str(tweet_id) + '\n')
            except UnicodeEncodeError:
                print tweet_id, data[hashtag][tweet_id]['text']

    match_file_contents = list()
    with open(match_file,'r') as match_obj:
        for line in match_obj:
            parts = line.split(',')
            match_file_contents.append(parts)


    i = 0
    while i < len(match_file_contents):
        with open(match_file_new, 'a') as write_obj:
            write_obj.write(','.join(match_file_contents[i]))
        # print(tweet_dict[match_file_contents[curr][0]])
        print(tweet_dict[match_file_contents[i][0]])
        j = i + 1
        print "i :", i
        try:
            while j < len(match_file_contents):
                if tweet_dict[match_file_contents[j][0]] == tweet_dict[match_file_contents[i][0]] and match_file_contents[j][1] == match_file_contents[i][1]:
                    print "j : ", j
                    del match_file_contents[j]
                j += 1
        except KeyError:
            print "Key not found"
        i += 1
        del match_file_contents[i]
    # a.make_unique_urls('../data/all_data/all_tweets.json','matchwindow.csv','matchwindow_unique.csv') - run this after writing log utils
    #  a.find_pos_tweets('../data/all_data/all_tweets.json','../data/all_data/url_details.json','../data/all_data/generate_samples/preprocessed1.json')


def process_window_size(match_file):
    #, new_file):
    percentages = list()
    positions = list()
    with open(match_file, 'r') as match_obj:
        for line in match_obj:
            parts = line.split(',')
            # parts.append(str(float(parts[2]) / float(parts[3]) * 100))
            # percentages.append(float(parts[5]))
            # positions.append(int(parts[2]))
            percentages.append(float(parts[2]))
            # with open(new_file, 'a') as new_obj:
            #    new_obj.write(parts[0] + ',' + parts[1] + ',' + parts[2] + ',' + parts[3] + ',' + parts[4].strip() + ',' + str(parts[5]) + '\n')
    # percentages_set = set(percentages)
    print np.mean(percentages)
    print np.std(percentages)
    # print np.mean(positions)
    # print np.std(positions)
    plt.bar(range(len(percentages)), sorted(percentages), align='center')
    # plt.bar(range(len(positions)), sorted(positions), align='center')
    plt.show()


def lcs_length(tweet, text):
    tweet_words = get_tweet_text(tweet).split()
    text_words = get_tweet_text(text).split()

    L = [[0 for j in range(len(tweet_words) + 1)] for i in range(len(text_words) + 1)]

    for i in range(len(text_words)):
        for j in range(len(tweet_words)):
            if text_words[i] == tweet_words[j]:
                L[i+1][j+1] = L[i][j] + 1
            else:
                L[i+1][j+1] = max(L[i+1][j], L[i][j+1])
    if len(tweet_words) == 0:
        return 0
    return float(L[len(text_words)][len(tweet_words)]) / float(len(tweet_words)) * 100
