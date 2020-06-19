from django.urls import path, include
from example_bot.apis.webhook import Webhook

urlpatterns = [
    path("webhook/", Webhook.as_view()),
]
