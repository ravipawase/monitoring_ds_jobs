import scrapy
from scrapy_playwright.page import PageCoroutine

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_coroutines": [
                        PageCoroutine("wait_for_selector", "body"),
                    ],
                },
            )

    def parse(self, response):
        self.logger.info("Page title: %s", response.css("title::text").get())