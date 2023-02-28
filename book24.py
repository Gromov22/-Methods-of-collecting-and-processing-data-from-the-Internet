import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from book24.items import Book24Item


class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    start_urls = ['https://book24.ru/best-price/?section_id=1357']

    def parse(self, response: HtmlResponse):
        for i in range(2, 6):
            next_page = f'https://book24.ru/best-price/page-{i}/?section_id=1357'
            yield response.follow(next_page, callback=self.parse)

        book_link = response.xpath('//div[@class="product-card__content"]/a/@href').getall()
        for link in book_link:
            yield response.follow(url=link, callback=self.parse_link)

    def parse_link(self, response: HtmlResponse):
        loader = ItemLoader(item=Book24Item(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('author', '//dd[@class="product-characteristic__value"]//text()')
        loader.add_xpath('price', '//span[@class="app-price product-sidebar-price__price-old"]/text()')
        loader.add_xpath('discont_price', '//span[@class="app-price product-sidebar-price__price"]/text()')
        loader.add_xpath('rating', '//span[@class="rating-widget__main-text"]/text()')
        loader.add_value('link', response.url)
        yield loader.load_item()
