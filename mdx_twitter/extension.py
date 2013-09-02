import logging

from markdown import Extension
from markdown.inlinepatterns import Pattern
from requests_oauthlib import OAuth1Session

TWITTER_LINK_RE = r"https?://twitter.com/([^/]+)/status(es)?/(?P<tweet_id>\d+)"


def get_cache_key(tweet_id):
    return u':'.join([u'mdx_twitter', unicode(tweet_id)])


class TwitterLinkPattern(Pattern):

    def get_html(self, tweet_id):
        html = None
        if self.ext.cache:
            html = self.ext.cache.get(get_cache_key(tweet_id))
        if not html:
            response = self.ext.client.get(
                "https://api.twitter.com/1.1/statuses/oembed.json",
                params={
                    'id': tweet_id,
                })
            result = response.json()
            if 'html' in result:
                html = result['html']
                if self.ext.cache:
                    self.ext.cache.set(get_cache_key(tweet_id), html, timeout=60*60*24)
            else:
                for err in result['errors']:
                    logging.warning(err['message'])
        if html:
            # if we have width in a config,
            # we are probably use Markdow in a UIWebView
            # https://dev.twitter.com/discussions/15450
            if self.ext.config['width'][0]:
                # let's fix the URL protocol
                html = html.replace(
                    '"//platform.twitter.com/',
                    '"https://platform.twitter.com/'
                )
                html = "<div style='width: %spx'>%s</div>" % (
                    self.ext.config['width'][0], html
                )
            return html
        return "[Tweet oembed error]"

    def handleMatch(self, m):
        tweet_id = m.group('tweet_id')
        html = self.get_html(tweet_id)
        placeholder = self.markdown.htmlStash.store(html, safe=True)
        return placeholder


class TwitterExtension(Extension):
    def __init__(self, configs, **kwargs):
        self.twitter_settings = kwargs.pop('twitter_settings')
        self.cache = kwargs.pop('cache')
        self.config = {
            'width': ['', 'Width of your tweet, useful for mobile'],
        }
        for key, value in configs:
            self.setConfig(key, value)

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = OAuth1Session(
                self.twitter_settings['CONSUMER_KEY'],
                client_secret=self.twitter_settings['CONSUMER_SECRET'],
                resource_owner_key=self.twitter_settings['ACCESS_TOKEN'],
                resource_owner_secret=self.twitter_settings['ACCESS_TOKEN_SECRET']
            )
        return self._client

    def extendMarkdown(self, md, md_globals):
        pattern = TwitterLinkPattern(TWITTER_LINK_RE, md)
        pattern.ext = self
        md.inlinePatterns.add('twitter_link', pattern, '<reference')
