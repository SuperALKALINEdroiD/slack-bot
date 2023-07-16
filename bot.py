import os
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import datetime
from util import Util
from connection import Connection
from job import Job
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import traceback

from sqlalchemy.orm import declarative_base
Base = declarative_base()

load_dotenv()
signing_secret = os.getenv('SIGNING_SECRET')

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)

utility = Util()
client = utility.create_slack_client()
bot_id = utility.get_bot_id()

connection = Connection('database.db')
engine = connection.get_engine()

try:
    Base.metadata.create_all(bind=engine)
    print('created table?')
except:
    traceback.print_exc()

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

        current_time = datetime.now()
        next_hour = current_time + timedelta(hours=1)
        next_hour_formatted = next_hour.strftime("%H:%M")
        print(type(next_hour_formatted))

        joined = Job(
            channelid=channel_id,
            joining_time=current_time,
            next_message_time=next_hour,
            next_message_time_string=next_hour_formatted
        )

        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(joined)
        session.commit()
        session.close()

if __name__ == '__main__':
    app.run(debug=True) # automatically reruns
