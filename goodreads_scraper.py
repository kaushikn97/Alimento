import scrapy

class ZomatoSpider(scrapy.Spider):
    name = 'zomato_spider'
    start_urls = ['https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once']

    def parse(self, response):
        SET_SELECTOR = '.col-l-12'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 a ::text'
            AREA_CLASS_SELECTOR = '.m5 pt5 clear'
            AREA_NAME_SELECTOR = 'a ::text'
            #MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            #IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'area': brickset.css(AREA_CLASS_SELECTOR).css(AREA_NAME_SELECTOR).extract_first(),
                #'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                #'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
