import json
import logging

from markdown import Extension
from markdown.inlinepatterns import Pattern
from requests_oauthlib import OAuth1Session

TWITTER_LINK_RE = r"https?://twitter.com/([^/]+)/status(es)?/(?P<tweet_id>\d+)"


def get_cache_key(params):
    return ":".join(
        ['mdx_twitter'] + [item for sublist in params.items() for item in sublist]
    )


def process_tweet(result, tweet_style='full'):
    html = result['html']
    if tweet_style not in ['full', 'simple']:
        module, function = tweet_style.rsplit('.', 1)
        return getattr(__import__(module), function)(result)
    return html


class TwitterLinkPattern(Pattern):

    def get_html(self, tweet_id):
        params = {
            'id': tweet_id,
        }
        tweet_style = 'full'
        if self.ext.config['style'][0]:
            tweet_style = self.ext.config['style'][0]
        if tweet_style != 'full':
            params['omit_script'] = 'true'
        result = None
        if self.ext.cache:
            result = self.ext.cache.get(get_cache_key(params))
            if result:
                result = json.loads(result)
        if not result:
            response = self.ext.client.get(
                "https://api.twitter.com/1.1/statuses/oembed.json",
                params=params
            )
            result = response.json()
            if 'html' in result:
                if self.ext.cache:
                    self.ext.cache.set(
                        get_cache_key(params),
                        json.dumps(result),
                        timeout=60*60*24
                    )
            else:
                for err in result['errors']:
                    logging.warning(err['message'])
        if result and 'html' in result:
            html = process_tweet(result, tweet_style)
            # if we have width in a config,
            # we are probably use Markdow in a UIWebView
            # https://dev.twitter.com/discussions/15450
            if tweet_style == 'full' and self.ext.config['width'][0]:
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
            'style': [
                '',
                'Style of the tweet: '
                'full, simple, or path to a function like "mdx_twitter.custom_style"'
            ],
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
