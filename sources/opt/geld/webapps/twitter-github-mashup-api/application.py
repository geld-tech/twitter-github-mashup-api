#!/usr/bin/env python
import json, os, sys
from flask import Flask, render_template


# Start Flask Application
app = Flask(__name__)
app.debug=True


# Flask App and Routes
@app.route("/")
def index(keyword=None):
	page_title="__PACKAGE_NAME__"
	page_domain="__PACKAGE_DOMAIN__"
	data=[]
	return render_template('index.html', page_title=page_title, page_domain=page_domain, keyword=section, data=data)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0')

