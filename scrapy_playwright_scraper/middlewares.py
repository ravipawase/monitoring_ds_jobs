import random

class ProxyMiddleware:
    def __init__(self):
        with open("scrapy_playwright_scraper/proxies/proxy_list.txt") as f:
            self.proxies = f.read().splitlines()

    def process_request(self, request, spider):
        if self.proxies:
            request.meta["proxy"] = random.choice(self.proxies)import random

class ProxyMiddleware:
    def __init__(self):
        with open("scrapy_playwright_scraper/proxies/proxy_list.txt") as f:
            self.proxies = f.read().splitlines()

    def process_request(self, request, spider):
        if self.proxies:
            request.meta["proxy"] = random.choice(self.proxies)