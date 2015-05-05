import data_structures
import simplejson as json


def convert_data_to_gflow (tweet_url_file, tweet_file, url_details, core_nlp_dir, op_path):
    with open(tweet_file,'r') as tweet_obj:
        data = json.load(tweet_obj)

    with open(url_details, 'r') as url_obj:
        urls_data = json.load(url_obj)

    tweet_to_url = {}
    with open(tweet_url_file, 'r') as tweet_url:
        for line in tweet_url:
            parts = line.split()
            if parts[0].strip() not in tweet_to_url.keys():
                tweet_to_url[parts[0].strip()] = [parts[1].strip()]
            else:
                tweet_to_url[parts[0].strip()].append(parts[1].strip())

    for hashtag in data:
        path = op_path + '/' + hashtag + '/original/'
        url_list = list()
        #use list comprehension for below?
        for tweet_id in data[hashtag].keys():
            if tweet_id in tweet_to_url:
                for url in tweet_to_url[tweet_id]:
                    if url not in url_list:
                        url_list.append(url)

        for url in url_list:
            #find url files in url_details and go write the file from it.
            write_file(path, urls_data[url])


def write_file(op_path, url_data) :
    filename = op_path + url_data['id'] + '.xml'
    # file_contents = '<DOC>\n<DATETIME>' + get_date(url_data['id']) + '</DATETIME>\n\n' \
    #               + '<TITLE'> + url_data['title'] + '</TITLE>\n\n<TEXT>' + url_data['text'] + '</TEXT>\n</DOC>'
    file_contents = '<DOC>\n\n' \
                    + '<TITLE'> + url_data['title'] + '</TITLE>\n\n<TEXT>' + url_data['text'] + '</TEXT>\n</DOC>'
    with open(filename, 'w') as f_obj:
        f_obj.write(file_contents)


defcore