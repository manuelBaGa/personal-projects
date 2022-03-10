import scrapy


class MorningstarSpider(scrapy.Spider):
    name = 'morningstar'
    allowed_domains = ['morningstar.com']
    start_urls = ['https://pythonscraping.com/linkedin/ietf.html']
    #start_urls = ['http://financials.morningstar.com/ratios/r.html?t=TMUS&region=usa&culture=en-US']

    def parse(self, response):
        title = response.xpath('//span[@class="title"]/text()').get()
        subtitle = response.xpath('//span[@class="subheading"]/text()').getall()
        return {"title":title, "subheading":subtitle}
