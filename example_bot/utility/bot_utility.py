import json
import logging
import requests
from messenger_bot.utility.util import MessengerUtility

from example_bot.config import BotConfig


class BotUtility:

    def __init__(self):
        self.bot_config = BotConfig()
        self.messenger_utility = MessengerUtility()
        self.url = self.bot_config.facebook_graph_api + self.bot_config.access_token

    def send_typing_on(self, user_id, typing_on: float = 2) -> None:
        """
        sends typing_on message on messenger. by default typing_on is 2 seconds
        """
        typing_on_payload = self.messenger_utility.typing_on(
            user_id, typing_on)
        self.send_message(typing_on_payload)
        import time
        time.sleep(typing_on)

    def send_message(self, payload) -> None:
        """
        This functions handels the messaging!
        """
        if payload is not None:
            status = requests.post(self.url, json=payload)
            if status is None:
                logging.error("Error - status is None")
            else:
                if status.status_code != 200:
                    logging.critical(status.text)

    def get_user_name(self, user_id: str) -> tuple:
        """
        gets the user details (first, last and middle name) from facebook's graph API using user_id
        """
        error_payload = (None,) * 3
        get_user_details_url = self.bot_config.facebook_profile_url + \
            user_id + '?access_token=' + self.bot_config.access_token

        user_details = requests.get(get_user_details_url)
        if user_details is None:
            return error_payload
        elif user_details.status_code == 200:
            user_details = user_details.json()
            print(user_details)

            first_name = user_details['first_name'] if 'first_name' in user_details else ''
            last_name = user_details['last_name'] if 'last_name' in user_details else ''
            gender = user_details['gender'] if 'gender' in user_details else ''
            return (first_name, last_name, gender)
        else:
            return error_payload
