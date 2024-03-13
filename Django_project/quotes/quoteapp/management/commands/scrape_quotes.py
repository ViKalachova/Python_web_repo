import scrapy

from datetime import datetime

from quoteapp.models import Author, Quote, Tag


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            tags = quote.css('div.tags a.tag::text').getall()
            author_name = quote.css('small.author::text').get()
            quote_text = quote.css('span.text::text').get()

            # Збереження або отримання автора з бази даних
            author, _ = Author.objects.get_or_create(fullname=author_name)

            # Створення цитати та додавання тегів
            new_quote = Quote.objects.create(artist=author, quote=quote_text)
            for tag in tags:
                tag_name = tag.strip()
                if tag_name:  # Перевірка, чи не порожній тег
                    existing_tag = Tag.objects.filter(tag_name=tag_name).first()
                    if existing_tag:
                        new_quote.tags.add(existing_tag)
                    else:
                        new_tag = Tag.objects.create(tag_name=tag_name)
                        new_quote.tags.add(new_tag)

        # Перехід на наступну сторінку
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class AuthorSpider(scrapy.Spider):
    name = "authors"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # Отримання даних автора
        fullname = extract_with_css('h3.author-title::text')
        born_date_str = extract_with_css('.author-born-date::text')
        born_location = extract_with_css('.author-born-location::text')
        description = extract_with_css('.author-description::text')

        # Перетворення формату дати у YYYY-MM-DD
        born_date = datetime.strptime(born_date_str, '%B %d, %Y').strftime('%Y-%m-%d')

        # Перевірка наявності автора у базі даних перед створенням
        author, _ = Author.objects.get_or_create(fullname=fullname, born_date=born_date, born_location=born_location,
                                                 description=description)


def main():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()

    process.crawl(AuthorSpider)
    process.crawl(QuotesSpider)
    process.start()