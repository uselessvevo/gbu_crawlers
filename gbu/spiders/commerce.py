# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider, IgnoreRequest

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest


class BaseCommerceSpider(scrapy.Spider):
    """ Строения (ОКС) """

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
        level=logging.INFO
    )

    def parse(self, response, **kwargs):
        if response.xpath('//*[contains(@class, "objects-desktop-list__not-found text-bold")]'):
            self.log('Wrong url')
            raise IgnoreRequest('Wrong url')

        self.log(f'Processing [{response.url}]')

        if not self.page_max:
            self.page_max = response.xpath('/html/body/div[1]/div[2]/div[2]/div/'
                                           'div[1]/div[2]/div/ul/li[7]/a//text()').get()
            self.page_max = int(self.page_max) if self.page_max else 1
            self.current_page = 2 if self.page_max > 1 else 1
            self.start_urls = [response.urljoin('?page=%s' % i) for i in range(1, self.page_max)]
            self.log(f'Total pages: {self.page_max}')

        # Get URLs from the current page
        container_urls = response.xpath(
            '//*[contains(@class, "templates-object-card__slider")]/@href'
        ).getall()

        for url in container_urls:
            # Iterate through the URLs
            page_url = response.urljoin(url)
            self.log(f'Parsing {page_url}')

            # Get data from the page
            yield SplashRequest(
                url=page_url,
                callback=self.parse_page,
                # endpoint='render.json',
                # args={'html': 1, 'png': 1, 'wait': 0.5}
            )

        # Next page
        next_page = response.xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/ul/li[8]/a/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.current_page += 1
            yield SplashRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                # endpoint='render.json',
                # args={'html': 1, 'png': 1, 'wait': 0.5}
            )

        # Close
        if self.current_page > self.page_max:
            raise CloseSpider(f'Done with {self.name}')

    def parse_page(self, response):
        """
        Метод обработки страницы объявления

        Args:
            response (object) - объект ответа запроса

        Yields:
            result (dict) - словарь с обработанной информацией
        """
        title, area = response.xpath('//*[contains(@class, "desk-object-title__name")]/text()').getall()
        area = area.lstrip().replace(',', '')

        address = response.xpath('//*[contains(@class, "desk-object-address__main")]/text()').getall()
        address = ''.join(address)

        price = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]'
                               '/div/div[2]/div/div/div/div[1]/div[1]/span/text()').get()

        price_m2 = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/'
                                  'div/div[2]/div/div/div/div[1]/div[2]/span[1]/text()').get()

        seller_fullname = response.xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/a/text()').get()

        text = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div/text()').get()

        contacts = response.xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[1]/div[4]/div/span/a/@href').get()
        contacts = contacts.split(':')[-1]

        slide_images = response.xpath('//*[contains(@class, "mediaslider__slide mediaslider__slide--rest")]/@style')
        slide_images = slide_images.re(r'background-image: url\(\/\/(.*?)\)')
        slide_images = [f'https://{i}' for i in slide_images[1:]]

        yield {
            'num_id_start': self.num_id_start,
            'title': title,
            'address': address,
            'area': area,
            'price': price,
            'price_m2': price_m2,
            'text': text,
            'contacts': contacts,
            'seller_fullname': seller_fullname,
            'url': response.request.url,
            'image_urls': slide_images,
            'kwargs': {
                'category': self.category,
                'name': self.name,
                'url': response.request.url,
                'number': self.num_id_start,
            }
        }

        self.num_id_start += 1

# Lands / ЗУ

LandAreasSpider = type('LandAreasSpider', (BaseCommerceSpider,), {
    'category': 'lands',
    'name': 'land_areas',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/zemelnye-uchastki/']
})

LandSpider = type('LandSpider', (BaseCommerceSpider,), {
    'category': 'lands',
    'name': 'land',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/zemlya/']
})

# Buildings / ОКС

OfficeSpider = type('OfficeSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'office',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/ofis/']
})

TradeBuildingSpider = type('TradeBuildingSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'trade_building',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/torgovye-pomeshheniya/']
})

FreeTradeBuildingSpider = type('FreeTradeBuildingSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'free_trade',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/svobodnoe-naznachenie/']
})

ReadyBusinessSpider = type('ReadyBusinessSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'ready_business',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/gotovyjj-biznes/']
})

ProductionBusinessSpider = type('ProductionBusinessSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'production',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/proizvodstvo/']
})

BaseBusinessSpider = type('BaseBusinessSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'base_business',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/bazy/']
})

StorageBusinessSpider = type('StorageBusinessSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'storage',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/sklad/']
})

FarmBusinessSpider = type('FarmBusinessSpider', (BaseCommerceSpider,), {
    'category': 'buildings',
    'name': 'farm',
    'num_id_start': 4200,
    'start_urls': ['https://www.etagi.com/commerce/ferma/']
})


process = CrawlerProcess(get_project_settings())
process.crawl(LandSpider)
process.crawl(LandAreasSpider)
process.crawl(OfficeSpider)
process.crawl(TradeBuildingSpider)
process.crawl(FreeTradeBuildingSpider)
process.crawl(ReadyBusinessSpider)
process.crawl(ProductionBusinessSpider)
process.crawl(StorageBusinessSpider)
process.crawl(FarmBusinessSpider)
process.start()
