import os
import re
import markdown
import json

from django.test import TestCase
from django.core.cache import cache

from mdx_twitter.extension import TWITTER_LINK_RE, get_cache_key

from httmock import urlmatch, HTTMock


@urlmatch(netloc=r'(.*\.)?twitter\.com$')
def twitter_mock(url, request):
    if 'omit_script' in request.url:
        return """{
            "html": "<blockquote class='twitter-tweet'><p>Need to plug in for a couple of hours? Here's the mix: 'NERO - Essential Mix (First broadcast Nov 2010)' - <a href='http://t.co/9MwHZCya' title='http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first'>soundcloud.com/nerouk/nero-es\\u2026</a></p>&mdash; Jason Costa (@jasoncosta) <a href='https://twitter.com/jasoncosta/status/240192632003911681' data-datetime='2012-08-27T21:02:40+00:00'>August 27, 2012</a></blockquote>\\n",
          "author_name": "Jason Costa",
          "provider_url": "http://twitter.com",
          "url": "https://twitter.com/jasoncosta/status/240192632003911681",
          "provider_name": "Twitter",
          "version": "1.0",
          "type": "rich",
          "height": null,
          "cache_age": "31536000000",
          "author_url": "https://twitter.com/jasoncosta",
          "width": 550}"""
    return """{
        "html": "<blockquote class='twitter-tweet'><p>Need to plug in for a couple of hours? Here's the mix: 'NERO - Essential Mix (First broadcast Nov 2010)' - <a href='http://t.co/9MwHZCya' title='http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first'>soundcloud.com/nerouk/nero-es\\u2026</a></p>&mdash; Jason Costa (@jasoncosta) <a href='https://twitter.com/jasoncosta/status/240192632003911681' data-datetime='2012-08-27T21:02:40+00:00'>August 27, 2012</a></blockquote>\\n<script src=\\"//platform.twitter.com/widgets.js\\" charset='utf-8'></script>",
      "author_name": "Jason Costa",
      "provider_url": "http://twitter.com",
      "url": "https://twitter.com/jasoncosta/status/240192632003911681",
      "provider_name": "Twitter",
      "version": "1.0",
      "type": "rich",
      "height": null,
      "cache_age": "31536000000",
      "author_url": "https://twitter.com/jasoncosta",
      "width": 550}"""


class TestDjangoInterations(TestCase):

    def test_django_caching(self):
        md = markdown.Markdown(extensions=['twitter'], safe_mode=True)
        key = get_cache_key({'id': '240192632003911681'})
        self.assertEqual(key, 'mdx_twitter:id:240192632003911681')
        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(json.loads(cache.get(key))['html'], html)

    def tearDown(self):
        cache.clear()


class TestMdxTwitter(TestCase):

    def test_regex_1(self):
        m = re.match(TWITTER_LINK_RE, "https://twitter.com/jasoncosta/status/240192632003911681")
        self.assertEqual(m.group('tweet_id'), '240192632003911681')

    def test_regex_2(self):
        m = re.match(TWITTER_LINK_RE, "http://twitter.com/jasoncosta/statuses/240192632003911681")
        self.assertEqual(m.group('tweet_id'), '240192632003911681')

    def test_oembed(self):
        md = markdown.Markdown(extensions=['twitter'])

        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            result = u"<blockquote class='twitter-tweet'><p>Need to plug in for a couple of hours? Here's the mix: 'NERO - Essential Mix (First broadcast Nov 2010)' - <a href='http://t.co/9MwHZCya' title='http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first'>soundcloud.com/nerouk/nero-es\u2026</a></p>&mdash; Jason Costa (@jasoncosta) <a href='https://twitter.com/jasoncosta/status/240192632003911681' data-datetime='2012-08-27T21:02:40+00:00'>August 27, 2012</a></blockquote>\n<script src=\"//platform.twitter.com/widgets.js\" charset='utf-8'></script>"  # NOQA
            self.assertEqual(html, result)

    def test_width(self):
        md = markdown.Markdown(extensions=['twitter(width=400)'])
        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertNotEqual(html.find('400px'), -1)
            self.assertNotEqual(html.find('https://platform.twitter.com/'), -1)

    def test_style_simple(self):
        md = markdown.Markdown(extensions=['twitter(style=simple)'])
        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(html.find('<script'), -1)

    def test_style_custom(self):
        md = markdown.Markdown(extensions=['twitter(style=mdx_twitter.custom_style)'])
        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(html.find('<script'), -1)
            self.assertEqual(html, u'<p><a href="https://twitter.com/jasoncosta/status/240192632003911681">Jason Costa:</a>Need to plug in for a couple of hours? Here\'s the mix: \'NERO - Essential Mix (First broadcast Nov 2010)\' - <a href="http://t.co/9MwHZCya" title="http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first">soundcloud.com/nerouk/nero-es\u2026</a></p>')

    if os.path.exists(os.path.expanduser('~/.mdx_twitter.cfg')):
        def test_live_oembed(self):
            import markdown
            md = markdown.Markdown(extensions=['twitter'], safe_mode=True)
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(html, u'<blockquote class="twitter-tweet"><p>Need to plug in for a couple of hours? Here&#39;s the mix: &quot;NERO - Essential Mix (First broadcast Nov 2010)&quot; - <a href="http://t.co/9MwHZCya">http://t.co/9MwHZCya</a></p>&mdash; Jason Costa (@jasoncosta) <a href="https://twitter.com/jasoncosta/statuses/240192632003911681">August 27, 2012</a></blockquote>\n<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>')  # NOQA

    def tearDown(self):
        cache.clear()
