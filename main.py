from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from spiders.GoogleSpider import GoogleSpider
from spiders.YandexSpider import YandexSpider
from utils.utils import *
from scrapy.utils.log import configure_logging

spiders = {
    "google": GoogleSpider,
    "yandex": YandexSpider
}


def load_scrapy_settings():
    import conf
    settings = {
        "DOWNLOAD_TIMEOUT": 10,
        "FEED_EXPORTERS": {
            "txt": "utils.exporter.TxtItemExporter"
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
            "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401
        }
    }
    if conf.use_random_proxy:
        # Retry many times since proxies often fail
        settings["RETRY_TIMES"] = 10
        # Retry on most error codes since proxies fail for different reasons
        settings["RETRY_HTTP_CODES"] = [500, 503, 504, 400, 403, 404, 408, 429, 302]

        settings["DOWNLOADER_MIDDLEWARES"] = {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 100,
            "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 101,
            "utils.randomProxy.RandomProxy": 102,
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 103
        }

        settings["PROXY_LIST"] = conf.path_to_proxy_list

        # Proxy mode
        # 0 = Every requests have different proxy
        # 1 = Take only one proxy from the list and assign it to every requests
        # 2 = Put a custom proxy to use in.txt the settings
        settings["PROXY_MODE"] = 0
        # If proxy mode is 2 uncomment this sentence :
        # settings["CUSTOM_PROXY"] = "https://127.0.0.1:8080"

    return settings


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="url parser", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-S", "--search-engine", help="Search engine to be used", default="google",
                        choices=spiders.keys())
    parser.add_argument("-M", "--metrics", help="metrics", choices=list(metrics.keys()) + [no_metrics_value],
                        default=no_metrics_value)
    parser.add_argument("-N", "--num", help="Number of results to be parsed for each request", default=8, type=int)
    parser.add_argument("-H", "--hints", action="store_true", help="Save hint for each request")
    parser.add_argument("request", nargs="+", help="File with requests to be parsed")
    config = vars(parser.parse_args())

    configure_logging()
    runner = CrawlerRunner(settings=load_scrapy_settings())

    for request in config["request"]:
        runner.crawl(spiders[config["search_engine"]], request=request, **config)
    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())

    reactor.run()
