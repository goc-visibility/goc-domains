import csv

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

    def __init__(self, known_domains: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if known_domains:
            try:
                with open(known_domains, 'r', encoding='utf-8') as domains_file:
                    csv_file = csv.reader(domains_file)
                    next(csv_file) # skip header
                    self.ids_seen = {domain[0] for domain in csv_file if domain}
            except FileNotFoundError as exc:
                logger.error('File %s not found', known_domains)

    def parse_item(self, response):
        scraped_bit = Domain()
        scraped_bit['domain'] = urllib.parse.urlparse(response.url).netloc
        yield scraped_bit
