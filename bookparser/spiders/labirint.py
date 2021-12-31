import scrapy
from scrapy.http import HtmlResponse

from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    # художественная лит-ра с кэшбеком
    start_urls = ['https://www.labirint.ru/genres/1852/?paperbooks=1&ebooks=1&otherbooks=1&available=1&preorder=1&price_min=&price_max=&cashback=1&form-pubhouse=&id_genre=1852&order=popularity&way=forward#catalog-navigation']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'pagination-next__text')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@id='catalog']//div[@data-product-id]//a[contains(@class, 'product-title-link')]")
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        authors = response.xpath("//div[contains(@class, 'authors')][1]/a//text()").getall()
        old_price = response.xpath("//div[contains(@class, 'buying-priceold')]//span//text()").get()
        discount_price = response.xpath("//div[contains(@class, 'buying-pricenew')]//span[1]//text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        url = response.url
        yield BookparserItem(
            name=name, authors=authors,
            old_price=old_price, discount_price=discount_price,
            rating=rating, url=url
        )
