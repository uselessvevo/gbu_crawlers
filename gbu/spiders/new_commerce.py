# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.utils.log import configure_logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class BaseEtagiSpider(CrawlSpider):
    category = None
    name = None
    num_id_start = None
    page_max = None
    current_page = None
    allowed_domains = ['www.etagi.com']

    configure_logging(install_root_handler=True)

    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.WARNING
    )

    rules = (
        Rule(LinkExtractor(allow=(f'{category}/\d+',)), callback='parse_page'),
    )

    def parse(self, response, **kwargs):
        self.log(f'Proccessing URL: {response.url}')
        import ipdb; ipdb.set_trace()


LandAreasSpider = type('LandAreasSpider', (BaseEtagiSpider,), {
    'category': 'lands',
    'name': 'land_areas',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/zemelnye-uchastki/']
})


# process = CrawlerProcess(get_project_settings())
# process.crawl(LandAreasSpider)
# process.start()