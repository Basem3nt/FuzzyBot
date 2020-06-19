from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from example_bot.models import BotUsers, MessageWatermarks


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BotUsers
        fields = ("facebook_id", "first_name", "last_name", "gender")

    def validate(self, attrs):
        """
        validate the payload of user if needed!
        """
        attrs["user_id"] = str(uuid4())[:12]
        attrs["last_contacted_at"] = timezone.now()
        attrs["user_status"] = "init"
        return attrs


class WatermarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageWatermarks
        fields = ("user", "watermark")

    def validate(self, attrs):
        attrs["message_id"] = str(uuid4())[:20]
        return attrs
