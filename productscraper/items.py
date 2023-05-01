import scrapy

class ProductItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    parent = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()