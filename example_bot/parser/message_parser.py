import json

from django.http import JsonResponse

from example_bot.reply.basic_reply import BasicReply
from example_bot.utility.constant import Constant


class Parser:

    def json_parser(self, incoming_message: list):
        """
        function receives incoming message and parses it
        Then sends it to appropriate functions of Parser class
        :incoming_message: list Json from facebook

        :returns message to facebook.
        """
        for entry in incoming_message[Constant.FB_ENTRY]:
            if Constant.FB_MESSAGING in entry:
                for message in entry[Constant.FB_MESSAGING]:
                    if Constant.FB_MESSAGE in message:
                        if Constant.FB_IS_ECHO in message[Constant.FB_MESSAGE]:
                            pass
                        elif Constant.FB_QUICK_REPLY in message[Constant.FB_MESSAGE]:
                            pass
                        elif Constant.FB_TAG_TEXT in message[Constant.FB_MESSAGE]:
                            BasicReply().basic_reply(message)
                        elif Constant.FB_TAG_READ in message[Constant.FB_MESSAGE]:
                            pass
                    elif Constant.FB_TAG_DELIVERY in message:
                        pass
                    elif Constant.FB_TAG_READ in message:
                        pass
                    elif Constant.FB_TAG_POSTBACK in message:
                        pass
                    else:
                        return
            elif Constant.FB_STANDBY in entry:
                pass
