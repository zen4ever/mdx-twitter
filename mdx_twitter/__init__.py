#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

__author__ = 'Andrii Kurinnyi'
__email__ = 'andrew@marpasoft.com'
__version__ = '0.2.6'


def makeExtension(configs=None):
    from .extension import TwitterExtension
    from .settings import get_twitter_settings
    try:
        from django.conf import settings
        if settings.configured:
            from django.core.cache import cache
        else:
            cache = None
            logging.warning('Django settings are not configured')
    except ImportError:
        cache = None
    return TwitterExtension(
        configs=configs,
        twitter_settings=get_twitter_settings(),
        cache=cache
    )


def custom_style(result):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(result['html'])
    tweet = soup.find('blockquote').find('p')
    link = soup.new_tag("a")
    link['href'] = result['url']
    link.string = result['author_name'] + ': '
    tweet.insert(
        0, link
    )
    return unicode(tweet)
