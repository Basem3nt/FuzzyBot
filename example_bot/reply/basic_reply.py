from django.http import JsonResponse
from messenger_bot.utility.util import MessengerUtility

from example_bot.nlp.basic import BasicNLP
from example_bot.sql_manager.helper import SqlHandler
from example_bot.utility.bot_utility import BotUtility
from example_bot.utility.constant import Constant


class BasicReply:

    def __init__(self):
        self.sql_handler = SqlHandler()
        self.bot_utility = BotUtility()
        self.basic_nlp = BasicNLP()
        self.messenger_utility = MessengerUtility()

    def basic_reply(self, message):
        """
        handles basic text reply from the USER!
        :param message:
        :return:
        """
        sender_id = message[Constant.FB_SENDER][Constant.FB_ID]
        timestamp = message["timestamp"]
        uniqueness_test = self.sql_handler.set_last_contacted_and_watermark(
            sender_id, timestamp)

        if not uniqueness_test:
            return JsonResponse({})

        if 'message' in message:
            nlp = message['message']['nlp'] if 'nlp' in message['message'] else None
            nlp_state = None
            if nlp is not None:
                text, nlp_state = self.basic_nlp.messenger_nlp(nlp)
                if text is not None:
                    text += " {}".format(
                        self.sql_handler.get_first_name(sender_id))
                    payload = self.messenger_utility.basic_text_reply_payload(
                        sender_id, text)
                    self.bot_utility.send_typing_on(sender_id, 2.5)
                    self.bot_utility.send_message(payload)

            if nlp_state in (None, "greetings"):
                """
                Only send the menu if it's a greeting or user sent a random message on board.
                """
                self.bot_utility.send_typing_on(sender_id, 2.5)
                # ---- TODO ----
                # payload = self.payload_generator.intro_generic_template(
                #     facebook_id=sender_id)
                # self.bot_utility.send_message(payload)
        else:
            print(message)
