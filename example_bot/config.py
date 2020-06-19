import os

from decouple import config

from FuzzyBot.settings import DEBUG


class BotConfig:

    """
    configuration file for example_bot app.

    Value of dev/debug will be taken from settings.py
    """

    def __init__(self):
        if DEBUG:
            self.__load_dev()
        else:
            self.__load_prod()

    def __dev_static(self):
        """
        This function initializes the static variables for dev
        """
        self.facebook_profile_url = "https://graph.facebook.com/"
        self.facebook_graph_api = "https://graph.facebook.com/v3.3/me/messages?access_token="

    def __load_dev(self):
        """
        load dev variables.
        """
        self.__dev_static()
        if config("VERIFY_TOKEN", None) is not None:
            self.verify_token = config("VERIFY_TOKEN")
        else:
            self.verify_token = os.environ.get("VERIFY_TOKEN", None)

        if config("PAGE_ACCESS_TOKEN", None) is not None:
            self.page_access_token = config("PAGE_ACCESS_TOKEN")
        else:
            self.page_access_token = os.environ.get("PAGE_ACCESS_TOKEN", None)

    def __load_prod(self):
        pass

    """
    load the getter in here
    """
    @property
    def messenger_verify_token(self):
        return self.verify_token

    @property
    def access_token(self):
        return self.page_access_token

    @property
    def profile_url(self):
        return self.facebook_profile_url

    @property
    def graph_api(self):
        return self.facebook_graph_api
