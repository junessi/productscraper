from datetime import datetime
import threading
from productscraper import utils
from productscraper.products_dumper import ProductsDumper

class ProductsPipeline(object):
    def __init__(self):
        print("initializing ProductsPipeline......")
        self.items = {}
        self.items_mutex = threading.Lock()

        self.root_item_id = ''
        self.start_time = datetime.now()

    def open_spider(self, spider):
        config = spider.config
        root_item = config.root_item
        self.items = {root_item['id']: root_item}

    def process_item(self, item, spider):
        with self.items_mutex:
            item_id = item['id'][0]
            item_name = item['name'][0]
            item_parent = item['parent'][0]
            item_type = item['type'][0]

            if item_type == 'Category':
                if item_id in self.items:
                    self.items[item_id]['id'] = item_id
                    self.items[item_id]['name'] = item_name
                    self.items[item_id]['parent'] = item_parent
                    self.items[item_id]['type'] = item_type
                else:
                    self.items[item_id] = {'id': item_id, 'name': item_name, 'parent': item_parent, 'type': item_type, 'categories': []}

                if item_parent not in self.items:
                    self.items[item_parent] = {'name': '', 'id': item_parent, 'parent': '', 'type': 'Category'}

                if 'categories' not in self.items[item_parent]:
                    self.items[item_parent]['categories'] = []

                self.items[item_parent]['categories'].append(item_id)
            elif item_type == 'Product':
                if item_parent not in self.items:
                    # this is only for root category
                    self.items[item_parent] = {'name': '', 'id': item_parent, 'parent': '', 'type': 'Category'}

                if 'products' not in self.items[item_parent]:
                    self.items[item_parent]['products'] = []

                item_brand = item['brand'][0]
                self.items[item_parent]['products'].append({'id': item_id,
                                                            'name': item_name,
                                                            'parent': item_parent,
                                                            'type': 'Product',
                                                            'brand': item_brand})

        return item

    def close_spider(self, spider):
        end_time = datetime.now()
        print("duration: {0}".format(end_time - self.start_time))
        ProductsDumper(spider.config, self.items).dump()

