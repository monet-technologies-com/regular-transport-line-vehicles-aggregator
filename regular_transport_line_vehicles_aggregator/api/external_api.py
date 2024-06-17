import json

import requests

from config import config


class Slack:
    slack_webhook = config.slack_webhook

    @classmethod
    def send_slack_message(self, message: str):
        message = {
            'text': message
        }

        response = requests.post(
            headers={'Content-Type': 'application/json'},
            url=self.slack_webhook, data=json.dumps(message)
            )

        if response.status_code == 200:
            print(f'Message sent successfully: {message}')
        else:
            print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')

        return response
