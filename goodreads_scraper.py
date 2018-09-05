import scrapy
import csv
from scrapy.selector import Selector
from bookClass import Book

class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads_spider'
    start_urls = []
    for i in range(1,11):
        start_urls.append('https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=' +str(i))

    def parse(self, response):

        table_rows = response.xpath('//*[contains(@class,"tableList")]//tr')
        data = {}

        links = table_rows[0].xpath('//*[contains(@class,"bookTitle")]/@href')
        for link in links:
            tempBook = Book(link.extract())
            tempBook.write_to_csv_link('data.csv')
        yield data
