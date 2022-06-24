import scrapy
from conf import folder_for_results
from time import sleep
from utils.utils import metrics, no_metrics_value, link_key


class AbstractSpider(scrapy.Spider):
    xpath_for_links = None
    req_headers = {}

    custom_settings = {
        "FEEDS": {folder_for_results + "/%(name)s.txt": {"format": "txt"}}
    }

    def __init__(self, request, search_engine, metrics, num, hints, input_file, **kwargs):
        self.name = request + "_" + search_engine + "_" + metrics + "-metrics" + ("_with-hints" if hints else "")
        super().__init__(self.name)
        self.request = request
        self.search_engine = search_engine
        self.metrics = metrics
        self.left = num
        self.hints = hints
        self.page = 0

    def start_requests(self):
        if self.hints:
            yield scrapy.Request(self.hints_url(), headers=self.req_headers,
                                 meta={"dont_redirect": True}, callback=self.parse_hints)
            sleep(0.5)
        yield scrapy.Request(self.search_url(), headers=self.req_headers, meta={"dont_redirect": True})

    def hints_url(self):
        raise NotImplementedError()

    def follow_url(self):
        raise NotImplementedError()

    def search_url(self):
        raise NotImplementedError()

    def new_link_found(self):
        pass

    def endOfPageReached(self):
        pass

    def checkLink(self, link):
        return True

    def parse_hints(self, response, **kwargs):
        raise NotImplementedError()

    def parse(self, response, **kwargs):
        if response is None:
            return
        for result in response.xpath(self.xpath_for_links):
            if self.left <= 0:
                break
            link = result.get()
            if link.startswith("https") and self.checkLink(link):
                self.left -= 1
                self.new_link_found()
                yield response.follow(url=link, callback=self.parse_link)
        if self.left > 0:
            self.endOfPageReached()
            sleep(0.5)
            newReq = response.follow(url=self.follow_url(),
                                     headers=self.req_headers,
                                     meta={"dont_redirect": True},
                                     callback=self.parse)
            if "proxy" in response.request.meta:
                newReq.meta["proxy"] = response.request.meta["proxy"]
                newReq.meta["exception"] = False
            yield newReq

    def parse_link(self, response, **kwargs):
        if self.metrics is not no_metrics_value:
            for xpath in metrics[self.metrics]:
                if response.xpath(xpath).get() is not None:
                    yield {link_key: response.url}
                    break
            return
        for xpath_list in metrics.values():
            for xpath in xpath_list:
                if response.xpath(xpath).get() is not None:
                    return
        yield {link_key: response.url}
        yield scr
