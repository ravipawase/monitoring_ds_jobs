BOT_NAME = "scrapy_playwright_scraper"

SPIDER_MODULES = ["scrapy_playwright_scraper.spiders"]
NEWSPIDER_MODULE = "scrapy_playwright_scraper.spiders"

# Enable Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Playwright settings
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

# User-Agent rotation
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Enable middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrapy_playwright_scraper.middlewares.ProxyMiddleware": 543,
}

# Configure a delay for requests to avoid IP blocking
DOWNLOAD_DELAY = 2