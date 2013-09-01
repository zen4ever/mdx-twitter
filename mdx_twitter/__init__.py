#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Andrii Kurinnyi'
__email__ = 'andrew@marpasoft.com'
__version__ = '0.1.0'


def makeExtension(*args):
    from .extension import TwitterExtension
    from .settings import get_twitter_settings
    return TwitterExtension(twitter_settings=get_twitter_settings())
