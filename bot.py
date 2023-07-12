import os
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import datetime
from util import Util
from shared_queue import get_shared_queue

load_dotenv()
signing_secret = os.getenv('SIGNING_SECRET')

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)

utility = Util()
client = utility.create_slack_client()
bot_id = utility.get_bot_id()

@slack_event_adapter.on('message')
def message(request):
    event = request.get('event', {})
    
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != bot_id:
        utility.send_message(client, channel_id, text)

@slack_event_adapter.on('member_joined_channel')
def joined_channel(request):
    event = request.get('event', {})

    user_id = event.get('user')
    channel_id = event.get('channel')

    if user_id == bot_id:
        utility.send_message(client, channel_id, "JOINED")

if __name__ == '__main__':
    app.run(debug=True) # automatically reruns
