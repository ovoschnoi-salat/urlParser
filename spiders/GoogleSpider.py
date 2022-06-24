import json
import re
from spiders.AbstractSpider import AbstractSpider
from utils.utils import google_ua, hints_key


class GoogleSpider(AbstractSpider):
    xpath_for_links = "//a[@href and h3]/@href"
    req_headers = {"User-Agent": google_ua}

    def hints_url(self):
        return f"https://www.google.com/complete/search?q={self.request}&client=gws-wiz"

    def search_url(self):
        return f"https://www.google.com/search?q={self.request}"

    def follow_url(self):
        return f"https://www.google.com/search?q={self.request}&start={self.page}"

    def new_link_found(self):
        self.page += 1

    def parse_hints(self, response, **kwargs):
        yield {hints_key: list(map(lambda x: re.sub(r"</?b>", "", x[0]), json.loads(response.text[19:-1])[0]))[1:]}
