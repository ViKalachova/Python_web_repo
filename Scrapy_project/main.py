import json

import scrapy
from itemadapter import ItemAdapter


class DataPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        elif 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {'ITEM_PIPELINES': {DataPipline: 300}}

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'tags': quote.css('div.tags a.tag::text').getall(),
                'author': quote.css('small.author::text').get(),
                'quote': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

class AuthorSpider(scrapy.Spider):
    name = "authors"
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {'ITEM_PIPELINES': {DataPipline: 300}}

    def parse(self, response):
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'fullname': extract_with_css('h3.author-title::text'),
            'born_date': extract_with_css('.author-born-date::text'),
            'born_location': extract_with_css('.author-born-location::text'),
            'description': extract_with_css('.author-description::text'),
        }

def main():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()

    process.crawl(QuotesSpider)
    process.crawl(AuthorSpider)
    process.start()


if __name__ == "__main__":
    main()