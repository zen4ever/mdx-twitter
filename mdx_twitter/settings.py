import os
import ConfigParser


def get_twitter_settings():
    TWITTER_SETTINGS = {
        'CONSUMER_KEY': '',
        'CONSUMER_SECRET': '',
        'ACCESS_TOKEN': '',
        'ACCESS_TOKEN_SECRET': '',
    }

    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(os.path.expanduser('~/.mdx_twitter.cfg')))
        for field in TWITTER_SETTINGS.keys():
            TWITTER_SETTINGS['field'] = config.get('Twitter', field)
    except IOError:
        pass
    return TWITTER_SETTINGS
