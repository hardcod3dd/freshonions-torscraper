# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import urlparse
import datetime
from tor_db import *
from collections import defaultdict
from datetime import *
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request
from scrapy.exceptions import NotConfigured


class FilterTooManySubdomainsMiddleware(object):
    def __init__(self):
        logger = logging.getLogger()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        return o

    @db_session
    def process_request(self, request, spider):

        if not Domain.is_onion_url(request.url):
            return None
        parsed_url = urlparse.urlparse(request.url)
        host = parsed_url.hostname
        subdomains = host.count(".")
        if subdomains > 2:
            raise IgnoreRequest("Too many subdomains (%d > 2)" % subdomains)

        return None


class FilterDeadDomainMiddleware(object):
    def __init__(self):
        logger = logging.getLogger()
        self.counter = defaultdict(int)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider_name = crawler.spider.name
        o = cls()
        return o

    @db_session
    def process_request(self, request, spider):

        # don't use this middleware while testing is site is up
        if hasattr(spider, "test") and spider.test == "yes":
            # logger = logging.getLogger()
            # logger.info("Testing mode, dead domains disabled")
            return None

        if not Domain.is_onion_url(request.url):
            return None

        domain = Domain.find_by_url(request.url)
        if not domain or domain.is_up:
            return None

        raise IgnoreRequest("Domain %s is dead, skipping" % domain.host)


class FilterNotScheduledMiddleware:
    def __init__(self, test_mode):
        self.test_mode = test_mode
        logger = logging.getLogger()
        logger.info(
            "FilterNotScheduledMiddleware loaded, test_mode %s" % str(test_mode)
        )

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider_name = crawler.spider.name
        test_mode = hasattr(crawler.spider, "test") and crawler.spider.test == "yes"
        o = cls(test_mode)
        return o

    @db_session
    def process_request(self, request, spider):
        parsed_url = urlparse.urlparse(request.url)

        if not self.test_mode or not parsed_url.path in ["/", ""]:
            return None

        if not Domain.is_onion_url(request.url):
            return None

        d = Domain.find_by_url(request.url)

        if d is None:
            return None

        now = datetime.now()

        if now > d.next_scheduled_check:
            return None
        else:
            raise IgnoreRequest(
                "FilterNotScheduledMiddleware: %s is not scheduled to check" % d.host
            )


class FilterDomainByPageLimitMiddleware(object):
    def __init__(self, max_pages):
        logger = logging.getLogger()
        logger.info(
            "FilterDomainbyPageLimitMiddleware loaded with MAX_PAGES_PER_DOMAIN = %d",
            max_pages,
        )
        self.max_pages = max_pages
        self.counter = defaultdict(int)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider_name = crawler.spider.name
        max_pages = settings.get("MAX_PAGES_PER_DOMAIN")
        o = cls(max_pages)
        return o

    def process_request(self, request, spider):

        parsed_url = urlparse.urlparse(request.url)
        host = parsed_url.hostname
        if self.counter[host] < self.max_pages:
            self.counter[host] += 1
            spider.logger.info("Page count is %d for %s" % (self.counter[host], host))
            return None
        else:
            raise IgnoreRequest(
                "MAX_PAGES_PER_DOMAIN reached, filtered %s" % request.url
            )


class AllowBigDownloadMiddleware(object):
    def __init__(self, big_download_size, allow_list):
        logger = logging.getLogger()
        logger.info(
            "AllowBigDownloadMiddleware loaded with BIG_DOWNLOAD_MAXSIZE = %d",
            big_download_size,
        )
        self.big_download_size = big_download_size
        self.allow_list = allow_list

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider_name = crawler.spider.name
        big_download_size = settings.get("BIG_DOWNLOAD_MAXSIZE")
        allow_list = settings.get("ALLOW_BIG_DOWNLOAD")
        o = cls(big_download_size, allow_list)
        return o

    def process_request(self, request, spider):

        parsed_url = urlparse.urlparse(request.url)
        host = parsed_url.hostname
        if host in self.allow_list:
            request.meta["download_maxsize"] = self.big_download_size
            logger = logging.getLogger()
            logger.info("Big download allowed for %s", host)
        return None


class InjectRangeHeaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("INJECT_RANGE_HEADER"):
            raise NotConfigured
        settings = crawler.settings
        big_download_maxsize = settings.get("BIG_DOWNLOAD_MAXSIZE", 0)
        allow_list = settings.get("ALLOW_BIG_DOWNLOAD", [])
        download_maxsize = settings.get("DOWNLOAD_MAXSIZE")
        return cls(download_maxsize, allow_list, big_download_maxsize)

    def __init__(self, download_maxsize, allow_list=[], big_download_maxsize=0):
        self.big_download_maxsize = (
            download_maxsize
            if big_download_maxsize < download_maxsize
            else big_download_maxsize
        )
        self.download_maxsize = download_maxsize
        self.allow_list = allow_list

    def process_spider_output(self, response, result, spider):
        def _set_range(r):
            if isinstance(r, Request):
                parsed_url = urlparse.urlparse(r.url)
                host = parsed_url.hostname
                max_size = (
                    self.big_download_maxsize
                    if host in self.allow_list
                    else self.download_maxsize
                )
                r.headers.setdefault("Range", "bytes=0-%d" % (max_size - 1))
            return r

        return (_set_range(r) for r in result or ())


class TorscraperSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
