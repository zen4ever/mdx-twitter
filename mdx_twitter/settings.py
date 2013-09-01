import os
import logging
import ConfigParser


def get_twitter_settings():
    TWITTER_SETTINGS = {
        'CONSUMER_KEY': '',
        'CONSUMER_SECRET': '',
        'ACCESS_TOKEN': '',
        'ACCESS_TOKEN_SECRET': '',
    }

    # if we are in a Django environment,
    # let's try to get settings from there
    try:
        from django.conf import settings
        if settings.configured:
            twitter_settings = getattr(settings, 'TWITTER_SETTINGS', None)
            if twitter_settings:
                return twitter_settings
    except ImportError:
        logging.warning('Django is not installed')

    # we are not in Django, or TWITTER_SETTINGS variable is absent
    # let's try to get it from config file
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.path.expanduser('~/.mdx_twitter.cfg')))
        for field in TWITTER_SETTINGS.keys():
            TWITTER_SETTINGS[field] = config.get('Twitter', field)
    except IOError:
        logging.warning('~/.mdx_twitter.cfg is missing')

    return TWITTER_SETTINGS
