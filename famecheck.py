#!/usr/bin/python
# author: bluescreenofjeff

# Thanks to Jan-Piet Mens, May 2015.  Slack slash command. (/whereis user)
# http://jpmens.net/2015/05/02/where-are-your-slack-team-members-at-the-moment/

import bottle   # pip install bottle
from bottle import request, response
import os.path #native
from os import system #native
from json import dumps
import random #native
import re #native
from time import sleep #native
import urllib2 #native
from bs4 import BeautifulSoup #pip install beautifulsoup4

botname = 'twitterbot'
app = application = bottle.Bottle()

# insert your Slack slash command token below
slack_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'

serverport = 8082


def post_message(message):
	rv = { "response_type": "in_channel", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

def post_ephemeral(message):
	rv = { "response_type": "ephemeral", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

snark = ['The stars are aligning! ', 'Get an autograph now. ', 'The fame train is a-comin. ', "Don't forget the little people. "]

#scrape current follower count from twitter
def twitterParse(handle):
	twitterurl = "https://www.twitter.com/"+handle.strip('@')

	try :
		web_page = urllib2.urlopen(twitterurl).read()
		soup = BeautifulSoup(web_page, 'html.parser')
		c = str(soup.find('a', {'data-nav':'followers'}).contents).split('data-count="')[1].split('"')[0]
		return post_message(random.choice(snark) + handle + " has " + c + " followers!")

	except:
		return post_ephemeral("Sorry, error retrieving follower count for "+handle)

@app.route('/', method='POST')
def slack_post():
	body = bottle.request.body.read()

	token           = request.forms.get('token')         
	team_id         = request.forms.get('team_id')       
	team_domain     = request.forms.get('team_domain')   
	service_id      = request.forms.get('service_id')    
	channel_id      = request.forms.get('channel_id')    
	channel_name    = request.forms.get('channel_name')  
	timestamp       = request.forms.get('timestamp')     
	user_id         = request.forms.get('user_id')       
	user_name       = request.forms.get('user_name')     
	text            = request.forms.get('text')          
	trigger_words   = request.forms.get('trigger_words')
	command			= request.forms.get('command')

	#validating token 
	if token != slack_token:  
		return post_ephemeral("Sorry bro, I'm broken - my token isn't right.")

	else:
		return twitterParse(text)


if __name__ == '__main__':
	while True:		
		bottle.run(app, host='0.0.0.0', port=serverport)


