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

    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.path.expanduser('~/.mdx_twitter.cfg')))
        for field in TWITTER_SETTINGS.keys():
            TWITTER_SETTINGS[field] = config.get('Twitter', field)
    except IOError:
        logging.warning('~/.mdx_twitter.cfg is missing')
    return TWITTER_SETTINGS
