import logging

from markdown import Extension
from markdown.inlinepatterns import Pattern
from requests_oauthlib import OAuth1Session

TWITTER_LINK_RE = r"https?://twitter.com/([^/]+)/status(es)?/(?P<tweet_id>\d+)"


def get_cache_key(tweet_id):
    return u':'.join([u'mdx_twitter', unicode(tweet_id)])


class TwitterLinkPattern(Pattern):

    def __init__(self, pattern, markdown_instance=None, client=None, cache=None):
        Pattern.__init__(self, pattern, markdown_instance)
        self.client = client
        self.cache = cache

    def get_html(self, tweet_id):
        if self.cache:
            html = self.cache.get(get_cache_key(tweet_id))
            if html:
                return html
        response = self.client.get("https://api.twitter.com/1.1/statuses/oembed.json", params={
            'id': tweet_id,
        })
        result = response.json()
        if 'html' in result:
            html = result['html']
            if self.cache:
                self.cache.set(get_cache_key(tweet_id), html)
            return html
        else:
            for err in result['errors']:
                logging.warning(err['message'])
        return "[Tweet oembed error]"

    def handleMatch(self, m):
        tweet_id = m.group('tweet_id')
        html = self.get_html(tweet_id)
        placeholder = self.markdown.htmlStash.store(html, safe=True)
        return placeholder


class TwitterExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.twitter_settings = kwargs.pop('twitter_settings')
        self.cache = kwargs.pop('cache')
        Extension.__init__(self, *args, **kwargs)

    def get_client(self):
        client = OAuth1Session(
            self.twitter_settings['CONSUMER_KEY'],
            client_secret=self.twitter_settings['CONSUMER_SECRET'],
            resource_owner_key=self.twitter_settings['ACCESS_TOKEN'],
            resource_owner_secret=self.twitter_settings['ACCESS_TOKEN_SECRET']
        )
        return client

    def extendMarkdown(self, md, md_globals):
        pattern = TwitterLinkPattern(TWITTER_LINK_RE, md, self.get_client(), cache=self.cache)
        md.inlinePatterns.add('twitter_link', pattern, '<reference')
