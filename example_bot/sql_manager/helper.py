import logging

from datetime import datetime
from uuid import uuid4

from django.utils import timezone

from example_bot.models import BotUsers, MessageWatermarks
from example_bot.sql_manager.serializer import (UserSerializer,
                                                WatermarkSerializer)
from example_bot.utility.bot_utility import BotUtility


class SqlHandler:

    def __init__(self):
        self.bot_utility = BotUtility()

    def get_user_object(self, facebook_id):
        """
        returns the user object with this particular user_id
        :param facebook_id: current facebook user_id
        :return:User Object
        """
        try:
            return BotUsers.objects.get(facebook_id=facebook_id)
        except BotUsers.DoesNotExist:
            return None

    def insert_new_user(self, facebook_id: str):
        """
        inserts a new user element inside the postgresql database
        :param facebook_id: current facebook_id of user
        :param username: pull the username from facebook using a simple get request later
        :return: modified_row
        """
        try:
            _ = BotUsers.objects.get(facebook_id=facebook_id)
            return _
        except BotUsers.DoesNotExist:
            # new user here
            user_data = self.bot_utility.get_user_name(facebook_id)
            if user_data[0] is not None:
                bot_user_serializer = UserSerializer(data={
                    "first_name": user_data[0],
                    "last_name": user_data[1],
                    "gender": user_data[2],
                    "facebook_id": facebook_id,
                })
                if bot_user_serializer.is_valid():
                    _ = bot_user_serializer.save()
                    return _
                else:
                    logging.error(bot_user_serializer.errors)

    def set_last_contacted_at(self, facebook_id):
        user = self.get_user_object(facebook_id)
        if user is not None:
            user.last_contacted_at = timezone.now()
            user.save()

    def get_first_name(self, facebook_id):
        """
        gets current username from the db
        :param user_id:
        :return:
        """
        return self.get_user_object(facebook_id).first_name

    def insert_msg_watermark(self, facebook_id, watermark):
        """
        inserts message watermark
        :param facebook_id: current user_id
        :param watermark: watermarked message
        :return: None
        """
        user_object = self.get_user_object(facebook_id)
        if user_object is not None:
            watermark_serializer = WatermarkSerializer(data={
                "user": user_object.pk,
                "watermark": watermark,
            })
            if watermark_serializer.is_valid():
                watermark_serializer.save()
            else:
                logging.error(watermark_serializer.errors)

    def is_watermark_unique(self, facebook_id, watermark):
        """
        checks if there is any entry of the current watermark by this user_id
        :param user_id: current user_id
        :param watermark: uniqueness of current message
        :return: :bool
        """
        try:
            MessageWatermarks.objects.get(user=self.get_user_object(facebook_id),
                                          watermark=watermark)
            return False
        except MessageWatermarks.DoesNotExist:
            return True

    def set_last_contacted_and_watermark(self, sender_id: str, timestamp: str):
        """
        This function will do the obvious work that has to be done in every function
        This will setup the last contacted at time for this user
        and then it will check the conversation watermark based on timestamp.
        If it's unique, this conversation/function will return True to proceed
        else, function will return False. which will result in HTTP 200 from the calling function 
        to avoid message looping

        sender_id: str
        timestamp: str

        returns: boolean
        """
        self.insert_new_user(sender_id)
        self.set_last_contacted_at(sender_id)
        if self.is_watermark_unique(sender_id, timestamp):
            """
            This uniqueness test helps prevents message looping.
            """
            self.insert_msg_watermark(sender_id, timestamp)
            return True
        else:
            # This is HTTP 200.
            return False
