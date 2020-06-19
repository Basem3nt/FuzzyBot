from django.db import models
from django.utils import timezone

# Create your models here.


class BotUsers(models.Model):
    user_id = models.CharField(max_length=12, primary_key=True)
    facebook_id = models.CharField(max_length=64, unique=True)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    is_spammer = models.BooleanField(default=False, verbose_name="Spammer")
    last_contacted_at = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        pass


class MessageWatermarks(models.Model):
    message_id = models.CharField(
        max_length=20, primary_key=True)
    user = models.ForeignKey(BotUsers, on_delete=models.DO_NOTHING)
    watermark = models.CharField(max_length=200, unique=True)


class MessageLogs(models.Model):
    message_id = models.CharField(
        max_length=20, primary_key=True)
    user = models.ForeignKey(BotUsers, on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=1000)
