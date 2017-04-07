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

botname = 'troll'

# insert your Slack slash command token below
slack_token = 'XXXXXXXXXXXXXXXXXXXXXXXX'

#optional settings
trollfile = 'troll_dict.txt'
serverport = 8080

troll_dict={}



global response

app = application = bottle.Bottle()

def parseTrolls(troll_file):
	with open(troll_file) as trolls:
		for eachline in trolls:
			key = eachline.split("%%")[0]
			value = eachline.split("%%")[1].strip("\n").strip("\r")

			if key in troll_dict.keys():
				troll_dict[key].append(value)
			else:
				troll_dict[key]=[value]

def post_message(message):
	rv = { "response_type": "in_channel", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

def post_ephemeral(message):
	rv = { "response_type": "ephemeral", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

def trollCompute(target,channel_name):
	# text contains the username (or it is empty)
	target = target.lower().rstrip()
	try:
		provided_name = target.split()[0]
		return post_message(random.choice(troll_dict[provided_name]))
	except:
		return post_ephemeral("Sorry bro, I don't have that name setup - blame my creator...")
	if (target.strip(' ') == '') or (target == None):
		return post_ephemeral("RTFM - need a name braj")
	else:
		return post_ephemeral("Sorry bro, I don't have that name setup - blame my creator...")

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
		return trollCompute(text,channel_name)


if __name__ == '__main__':
	parseTrolls(trollfile)
	while True:		
		bottle.run(app, host='0.0.0.0', port=serverport)
