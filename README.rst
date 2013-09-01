===============================
Markdown Twitter Extension
===============================

.. image:: https://badge.fury.io/py/mdx-twitter.png
    :target: http://badge.fury.io/py/mdx-twitter
    
.. image:: https://travis-ci.org/zen4ever/mdx-twitter.png?branch=master
        :target: https://travis-ci.org/zen4ever/mdx-twitter

.. image:: https://pypip.in/d/mdx-twitter/badge.png
        :target: https://crate.io/packages/mdx-twitter?version=latest


Markdown extension for embedding tweets using twitter OEmbed API

* Free software: BSD license
* Documentation: http://mdx-twitter.rtfd.org.

How to use
----------

Allows you to embed tweets into your Markdown.

Just install the package:

    .. code-block:: bash

        pip install mdx-twitter

Because Twitter API 1.1 requires you to authenticate, you will need to create
a config file with your credentials at '~/.mdx_twitter.cfg'::

    [Twitter]
    CONSUMER_KEY=xxxxxxxxxxxx
    CONSUMER_SECRET=xxxxxxxxxxxx
    ACCESS_TOKEN=xxxxxxxxxxxx
    ACCESS_TOKEN_SECRET=xxxxxxxxxxxx

Then just add 'twitter' to the list of your extensions:

    .. code-block:: python

        import markdown

        md = markdown.Markdown(extensions=['twitter'])

Twitter urls in your Makdown will become embedded tweets::

        https://twitter.com/jasoncosta/status/240192632003911681

Django integration
------------------

Since Twitter has a rate limit on their APIs, and doing network calls all the
time just to render Markdown is a bad idea anyways, we would need some caching.

If you are using `mdx-twitter` in a Django project, it will automatically
use your cache settings to cache HTML returned from Twitter API.

Also, you could place your API credentials in TWITTER_SETTINGS variable in your
project's `settings.py`, instead of using .cfg file

    .. code-block:: python

        TWITTER_SETTINGS = {
            'CONSUMER_KEY': '',
            'CONSUMER_SECRET': '',
            'ACCESS_TOKEN': '',
            'ACCESS_TOKEN_SECRET': '',
        }
