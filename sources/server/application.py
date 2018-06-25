#!/usr/bin/env python
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug=True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search/<keyword>")
def hi(keyword=None):
    if keyword:
        return jsonify({"data": []}), 200
    else:
        return jsonify({"data": []}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')

#!/usr/bin/env python
"""
	API mashup of GitHub and Twitter APIs
    Search for "KEYWORD" projects on GitHub, then for each project search for tweets that mention it.
	Outputs summary of each project with a short list of recent tweets (JSON format)

	./py-mashup-api.py --consumerkey <CONSUMER_KEY> --consumersecret <CONSUMER_SECRET> --keyword <KEYWORD>
	
"""

import base64
import datetime
import csv
import json
import io
import logging
import logging.handlers
import os
from optparse import OptionParser
import oauth2
import platform
import Queue
import re
import requests
from requests.auth import HTTPBasicAuth
import subprocess
import sys
import threading
import time
import urllib
import urllib2

# Twitter Application Access Token and Secret
twitter_access_token=""
twitter_access_secret=""

# Globals
github_api_uri="https://api.github.com/search/repositories?q="
github_projects_limit=10
twitter_api_uri_timeline='https://api.twitter.com/1.1/statuses/home_timeline.json'
twitter_api_uri_search='https://api.twitter.com/1.1/search/tweets.json'

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s',level=logging.INFO)
logger = logging.getLogger('root')

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=key, secret=secret)
    token = oauth2.Token(key=twitter_access_token, secret=twitter_access_secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

# Functions
def main():
    tweets_list=[]
    try:
        # Parse options
        parser = OptionParser()
        parser.add_option('--consumerkey', action='store', dest='twitter_consumer_key', help='Twitter Consumer Key.')
        parser.add_option('--consumersecret', action='store', dest='twitter_consumer_secret', help='Twitter Consumer Secret.')
        parser.add_option('--keyword', action='store', dest='keyword', help='Keyword to search Github for and to identify in Twitter.')
        parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
        options, args = parser.parse_args()
        if not options.twitter_consumer_key:
            parser.error('Twitter Consumer Key not provided, use -h to show the help')
        if not options.twitter_consumer_secret:
            parser.error('Twitter Consumer Secret not provided, use -h to show the help')
        if not options.keyword:
            parser.error('Keyword not provided, use -h to show the help')
        if options.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug('Enabled DEBUG logging level.')
        logger.info('Options parsed')
        
	# GitHub Query
	logger.info('Querying GitHub for %s' % options.keyword)
	github_query_url = "%s%s" % (github_api_uri, options.keyword)
	response = urllib.urlopen(github_query_url)
	data = json.loads(response.read())
        
        # Twitter Client
	logger.info('Search for tweets mentioning the GitHub projects identified by the keyword "%s"..' % options.keyword)
	for item in data.get("items")[:github_projects_limit]:
		twitter_search_tweets_url="%s?q=%s" % (twitter_api_uri_search, item.get("full_name"))
		data = oauth_req(twitter_search_tweets_url, options.twitter_consumer_key, options.twitter_consumer_secret)
		tweets = json.loads(data)
		logger.info("Retrieved %d tweets mention the GitHub project %s" % (len(tweets['statuses']), item.get("full_name")))
		for tweet in tweets['statuses']:
			logger.debug(tweet)
			tweets_list.append(tweet)
	
	logger.info('Retrieved %s tweets mentioned the projects identified by the keyword "%s"'% (len(tweets_list), options.keyword))
	logger.debug('JSON contents dump: %s' % json.dumps(tweets_list, ensure_ascii=False))

	filename="%s.json" % options.keyword
	with io.open(filename, 'w', encoding='utf-8') as f:
		f.write(json.dumps(tweets_list, ensure_ascii=False))

	logger.info('Written result to file %s'% (filename))
 
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('Exception %s in %s at line %d: %s' % (exc_type, fname, exc_tb.tb_lineno, e))

# Main
if __name__ == '__main__':
    logger.info('Starting processing')
    main()

