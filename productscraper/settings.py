SPIDER_MODULES = ['productscraper.spiders']

ITEM_PIPELINES = {
    'productscraper.pipelines.ProductsPipeline': 100,
}

COOKIES_ENABLED = False
COOKIES_DEBUG = False
