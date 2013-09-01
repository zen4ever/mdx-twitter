import os
import re
import markdown

from django.test import TestCase
from django.core.cache import cache

from mdx_twitter.extension import TWITTER_LINK_RE, get_cache_key

from httmock import urlmatch, HTTMock


@urlmatch(netloc=r'(.*\.)?twitter\.com$')
def twitter_mock(url, request):
    return """{
        "html": "<blockquote class='twitter-tweet'><p>Need to plug in for a couple of hours? Here's the mix: 'NERO - Essential Mix (First broadcast Nov 2010)' - <a href='http://t.co/9MwHZCya' title='http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first'>soundcloud.com/nerouk/nero-es\\u2026</a></p>&mdash; Jason Costa (@jasoncosta) <a href='https://twitter.com/jasoncosta/status/240192632003911681' data-datetime='2012-08-27T21:02:40+00:00'>August 27, 2012</a></blockquote>\\n<script src='//platform.twitter.com/widgets.js' charset='utf-8'></script>",
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

    def setUp(self):
        pass

    def test_django_caching(self):
        md = markdown.Markdown(extensions=['twitter'], safe_mode=True)
        key = get_cache_key('240192632003911681')
        with HTTMock(twitter_mock):
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(cache.get(key), html)

    def tearDown(self):
        cache.clear()


class TestMdxTwitter(TestCase):

    def setUp(self):
        pass

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
            result = u"<blockquote class='twitter-tweet'><p>Need to plug in for a couple of hours? Here's the mix: 'NERO - Essential Mix (First broadcast Nov 2010)' - <a href='http://t.co/9MwHZCya' title='http://soundcloud.com/nerouk/nero-essential-mix-first?utm_source=soundcloud&amp;utm_campaign=share&amp;utm_medium=twitter&amp;utm_content=http://soundcloud.com/nerouk/nero-essential-mix-first'>soundcloud.com/nerouk/nero-es\u2026</a></p>&mdash; Jason Costa (@jasoncosta) <a href='https://twitter.com/jasoncosta/status/240192632003911681' data-datetime='2012-08-27T21:02:40+00:00'>August 27, 2012</a></blockquote>\n<script src='//platform.twitter.com/widgets.js' charset='utf-8'></script>"  # NOQA
            self.assertEqual(html, result)

    if os.path.exists(os.path.expanduser('~/.mdx_twitter.cfg')):
        def test_live_oembed(self):
            import markdown
            md = markdown.Markdown(extensions=['twitter'], safe_mode=True)
            html = md.convert('http://twitter.com/jasoncosta/statuses/240192632003911681')
            self.assertEqual(html, u'<blockquote class="twitter-tweet"><p>Need to plug in for a couple of hours? Here&#39;s the mix: &quot;NERO - Essential Mix (First broadcast Nov 2010)&quot; - <a href="http://t.co/9MwHZCya">http://t.co/9MwHZCya</a></p>&mdash; Jason Costa (@jasoncosta) <a href="https://twitter.com/jasoncosta/statuses/240192632003911681">August 27, 2012</a></blockquote>\n<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>')  # NOQA

    def tearDown(self):
        cache.clear()
