import urllib
import json

response = urllib.urlopen("https://api.twitter.com/1.1/search/tweets.json?q=%23FreeCoffee")
print json.load(response)
