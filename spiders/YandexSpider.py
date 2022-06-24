import json

from spiders.AbstractSpider import AbstractSpider
from utils.utils import hints_key


class YandexSpider(AbstractSpider):
    xpathForLinks = "//a[(contains(@class, 'OrganicTitle-Link') or contains(@class, 'serp-item__title-link')) and @href]/@href"

    def checkLink(self, link):
        return not link.startswith("https://yabs.yandex.ru/count")

    def hints_url(self):
        return f"https://yandex.ru/suggest/suggest-ya.cgi?part={self.request}"

    def search_url(self):
        return f"https://yandex.ru/search/?lr=2&text={self.request}"

    def follow_url(self):
        return f"https://yandex.ru/search/?lr=2&text={self.request}&p={self.page}"

    def endOfPageReached(self):
        self.page += 1

    def parse_hints(self, response, **kwargs):
        yield {hints_key: json.loads(response.text[14:-4])[1]}
