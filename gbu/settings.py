# Scrapy settings for gbu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from shutil import which


BOT_NAME = 'gbu'

NEWSPIDER_MODULE = 'gbu.spiders'

SPIDER_MODULES = ['gbu.spiders']

SPIDERS_LIST = [
    'lands'
    'buildings',
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
}

DOWNLOADER_MIDDLEWARES = {
    # 'gbu.middlewares.GbuSeleniumMiddleware': 800,
    # 'scrapy_selenium.SeleniumMiddleware': 800,
    # 'gbu.middlewares.GbuSpiderMiddleware': 543,
}

ITEM_PIPELINES = {
    'gbu.pipelines.GbuImagesPipeline': 100,
}

FEED_EXPORTERS = {
    'xlsx': 'gbu.exporters.CustomExcelExporter',
}

FEEDS = {
    'output/%(name)s/%(name)s_%(time)s.xlsx': {
        'format': 'xlsx',
        'overwrite': False
    }
}

# FEED_EXPORT_FIELDS = ['num_id_start', 'title', 'address', 'area', 'price',
#                        'price_m2', 'text', 'contacts', 'seller_fullname', 'url']

IMAGES_STORE = 'output'

# Selenium
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = 'bin/chromedriver.exe'
