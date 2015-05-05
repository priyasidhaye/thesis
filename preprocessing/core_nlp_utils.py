import simplejson as json


def separate_articles(articles_url):
    with open(articles_url, 'r') as articles_obj:
        data = json.load(articles_obj)
    file_list_name = 'file_list'
    for url_id in data:
        article_text = data[url_id]['text']
        filename = 'articles/' + url_id
        with open(filename, 'w') as art_op_obj:
            art_op_obj.write(article_text.encode('utf-8'))
        with open(file_list_name, 'a') as file_list_obj:
            file_list_obj.write('articles/' + url_id + '\n')

