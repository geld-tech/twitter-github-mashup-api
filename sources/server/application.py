#!/usr/bin/env python
"""
	API mashup of GitHub and Twitter APIs
    Search for "KEYWORD" projects on GitHub, then for each project search for tweets that mention it.
	Outputs summary of each project with a short list of recent tweets (JSON format)

"""
import base64
import csv
import ConfigParser
import datetime
from dependencies import oauth2
import json
import logging
import logging.handlers
import os
from optparse import OptionParser
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
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug=True

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))
twitter_api_url_timeline=config.get('twitter', 'api_url_timeline')
twitter_api_url_search=config.get('twitter', 'api_url_search')
twitter_access_token=config.get('twitter', 'access_token')
twitter_access_secret=config.get('twitter', 'access_secret')
twitter_consumer_key=config.get('twitter', 'consumer_key')
twitter_consumer_secret=config.get('twitter', 'consumer_secret')
github_api_url=config.get('github', 'api_url')
github_projects_limit=config.getint('github', 'limit')

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s',level=logging.INFO)
logger = logging.getLogger('root')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search/<keyword>")
def hi(keyword=None):
    if keyword:
        data = getProjectsTweets(keyword)
        return jsonify({"data": data}), 200
    else:
        return jsonify({"data": []}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    global twitter_access_token
    global twitter_access_secret
    consumer = oauth2.Consumer(key=key, secret=secret)
    token = oauth2.Token(key=twitter_access_token, secret=twitter_access_secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def getProjectsTweets(keyword):
    global github_api_url
    global github_projects_limit
    global twitter_api_url_timeline
    global twitter_api_url_search
    global twitter_consumer_key
    global twitter_consumer_secret
    projects_tweets_data={}
    try:
        # GitHub Query
        logger.info('Querying GitHub for %s' % keyword)
        github_query_url = "%s%s" % (github_api_url, keyword)
        response = urllib.urlopen(github_query_url)
        data = json.loads(response.read())
        
        # Twitter Client
        logger.info('Search for tweets mentioning the GitHub projects identified by the keyword "%s" (limit=%d) ..' % (keyword, github_projects_limit))
        for item in data.get("items")[:github_projects_limit]:
            tweets_list=[]
            twitter_search_tweets_url="%s?q=%s" % (twitter_api_url_search, item.get("full_name"))
            data = oauth_req(twitter_search_tweets_url, twitter_consumer_key, twitter_consumer_secret)
            tweets = json.loads(data)
            if 'statuses' in tweets:
                logger.info("Retrieved %d tweets mention the GitHub project %s" % (len(tweets['statuses']), item.get("full_name")))
                for tweet in tweets['statuses']:
                    logger.debug(tweet)
                    tweets_list.append(tweet)
            else:
                logger.info("No tweets found mentioning the GitHub project %s" % (item.get("full_name")))
            projects_tweets_data[item.get("full_name")]=tweets_list
        
        logger.info('Retrieved %s tweets mentioning the projects identified by the keyword "%s"'% (len(tweets_list), keyword))
        logger.debug('JSON contents dump: %s' % json.dumps(tweets_list, ensure_ascii=False))

        return projects_tweets_data
 
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('Exception %s in %s at line %d: %s' % (exc_type, fname, exc_tb.tb_lineno, e))

if __name__ == "__main__":
    # Parse options
    parser = OptionParser()
    parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0')

