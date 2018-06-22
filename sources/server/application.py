#!/usr/bin/env python
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug=True

@app.route("/")
@app.route("/hello")
def index():
    return render_template('index.html')

@app.route("/hi")
@app.route("/hi/<name>")
def hi(name=None):
    if name:
        return jsonify({"data": "hi, %s" % name}), 200
    else:
        return jsonify({"data": "hi"}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')

