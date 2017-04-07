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
from threading import Thread

# insert your Slack slash command token and incoming webhook URL below
slack_token = 'XXXXXXXXXXXXXXXXXXXXXXXX'
webhookURL = 'https://hooks.slack.com/services/AAAAAAAAA/BBBBBBBBB/CCCCCCCCCCCCCCCCCCCCCCCC'

#optional settings
storyfile = 'story.txt'
serverport = 8081

#bot settings
bot_username = 'Spooky StoryBot'
bot_emoji = ':ghost:'

global response

app = application = bottle.Bottle()

def post_message(message):
	rv = { "response_type": "in_channel", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

def post_ephemeral(message):
	rv = { "response_type": "ephemeral", "text": message }
	response.content_type = 'application/json'
	return dumps(rv)

def storytime(channelname):
	with open(storyfile) as story:
		for eachline in story:
			sleep(random.randint(3,9))
			payload = '''{"username": "''' + bot_username +'''", "icon_emoji": "''' + bot_emoji +'''", "channel": "'''+channelname+'''", "text": "'''+eachline.strip('\n').strip('\r')+'''"}''' 
			command = '''curl -X POST --data-urlencode payload=''' + dumps(payload) + ' ' + webhookURL
			system(command)

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
		t = Thread(target=storytime, args=(channel_name,))
		t.start()
		return post_ephemeral("One story coming up!")

if __name__ == '__main__':
	while True:		
		bottle.run(app, host='0.0.0.0', port=serverport)