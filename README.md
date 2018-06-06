# twitter-github-mashup-api

## Status

[![Download](https://api.bintray.com/packages/geldtech/debian/twitter-github-mashup-api/images/download.svg)](https://bintray.com/geldtech/debian/twitter-github-mashup-api#files)
[![Build Status](https://travis-ci.org/geld-tech/twitter-github-mashup-api.svg?branch=master)](https://travis-ci.org/geld-tech/twitter-github-mashup-api)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Description

Twitter/GitHub APIs Mashup Application built in Python Flask

## Demo

A sample demo of the project is hosted on <a href="http://geld.tech">geld.tech</a>.


## Usage

* Install the repository information and associated GPG key (to ensure authenticity):
```
$ echo "deb https://dl.bintray.com/geldtech/debian /" | sudo tee -a /etc/apt/sources.list.d/geld-tech.list
$ sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com EA3E6BAEB37CF5E4
```

* Update repository list of available packages and clean already installed versions
```
$ sudo apt update
$ sudo apt clean
```

* Install package
```
$ sudo apt install twitter-github-mashup-api
```

* Reload services and start ours
```
$ sudo systemctl daemon-reload
$ sudo systemctl start twitter-github-mashup-api
$ sudo systemctl status twitter-github-mashup-api
```

## Settings

The following environment variables need to be configured in the Travis CI settings page to ensure a good build and deployment:

```
- BINTRAY_USER		Username used to upload to Bintray
- BINTRAY_API_KEY	API Key used to upload in Bintray
- BINTRAY_SUBJECT	User or organisation used to upload in Bintray
- GA_UA_ID		Google Analytics User ID
```
