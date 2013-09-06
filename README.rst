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

Embedding tweets in UIWebView
-----------------------------

There are currently some problems with embedding tweets in UIWebView.

* Protocol agnostic src attribute "//platform.twitter.com/widgets.js" doesn't
  allow script to load

* There seems to be a problem with automatically determining width of the
  container

  https://dev.twitter.com/discussions/15450

So there is a 'width' configuration option that offers a quick 'fix' for those
problems. Just specify expected width of your tweet in pixels. 

    .. code-block:: python

        import markdown

        md = markdown.Markdown(extensions=['twitter(width=300)'])

It will only work with 'style' full.

Styles
------

You can customize appearance of your tweets using 'style' configuration
options. Default style is 'full', which includes script javascript, you could
also use 'simple' style, which just includes tweet in a blockquote tag without
javascript.

Another option would be to specify a path to your own function, which accepts
Twitter response json as an argument and should return final html.

An example custom style is included in the library. You can use it by
specifying 'style=mdx_twitter.custom_style'

TODO
----

* If we embed multiple tweets, we don't need to have `script` tag after each
  tweet. We should probably just have a `script` tag at the end of the
  document.
