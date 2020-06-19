import logging

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from example_bot.config import BotConfig
from example_bot.parser.message_parser import Parser


class Webhook(APIView):

    def get(self, request):
        verify_token = request.GET.get("hub.verify_token", "no_verify_token")
        challenge = request.GET.get("hub.challenge", "no_challenge")
        # It does nothing now. But keeping it anyway!
        mode = request.GET.get("hub.mode", "no_mode")

        if verify_token == BotConfig().messenger_verify_token:
            return HttpResponse(challenge)
        else:
            return JsonResponse({
                "status": 'Access Restricted',
            }, status=401)

    def post(self, request):
        incoming_message = request.data
        try:
            Parser().json_parser(incoming_message)
        except ValueError as error:
            print("Webhook - ValueError - {}".format(error))
            logging.exception("Webhook value error")
        except Exception as error:
            print("Webhook - Exception - {}".format(error))
            logging.exception("Webhook Exception error")
        finally:
            # return a final blank HttpResponse in case, there is no reply from above conditions
            # blank JsonResponse will send a HTTP 200 stating that the request has been handled and taken care of.
            return JsonResponse({})
