import os
from dotenv import load_dotenv
import slack

class Util:
    def __init__(self):
        load_dotenv()
        self.client = None
        self.slack_token = os.getenv('SLACK_TOKEN')

    def create_slack_client(self):
        self.client = slack.WebClient(token=self.slack_token)

    def get_slack_client(self):
        return self.client

    def get_bot_id(self):
        return self.client.api_call('auth.test')['user_id']

    def send_message(self, client, channel_id, text):
        try:
            self.client.chat_postMessage(channel=channel_id, text=f'{text}')
            return True
        except:
            False
