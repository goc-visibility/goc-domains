import urllib.parse

from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field
from scrapy.spiders import Rule


class Domain(Item):
    domain = Field()


class CanadaSpider(CrawlSpider):
    name = "canada"

    start_urls = [
        'https://www.canada.ca/en.html',
        'https://www.canada.ca/fr.html',
    ]

    rules = [
        Rule(LinkExtractor(allow_domains=('canada.ca','gc.ca')), callback='parse_item', follow=True),
    ]

    def parse_item(self, response):
        scraped_bit = Domain()
        scraped_bit['domain'] = urllib.parse.urlparse(response.url).netloc
        yield scraped_bit
