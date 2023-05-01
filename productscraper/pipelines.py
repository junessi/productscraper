from datetime import datetime
import threading
import json

class ProductsPipeline(object):
    def __init__(self):
        print("initializing ProductsPipeline......")
        self.items = {}
        self.items_mutex = threading.Lock()

        self.root_item_id = ''

    def open_spider(self, spider):
        self.root_item_id = spider.root_item['id']
        self.items = {self.root_item_id: spider.root_item}
        self.start_time = datetime.now()

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
                    self.items[item_parent] = {'name': '', 'id': item_parent, 'parent': '', 'type': 'Category'}

                if 'products' not in self.items[item_parent]:
                    self.items[item_parent]['products'] = {}

                item_brand = item['brand'][0]
                if item_brand and item_brand not in self.items[item_parent]['products']:
                    self.items[item_parent]['products'][item_brand] = []

                self.items[item_parent]['products'][item_brand].append({'id': item_id, 'name': item_name, 'parent': item_parent, 'type': 'Product', 'brand': item_brand})

        return item

    def close_spider(self, spider):
        end_time = datetime.now()
        print("duration: {0}".format(end_time - self.start_time))
        with open("kramp.json", "w") as f:
            f.write(json.dumps(self.items))
        self.print_item_tree(self.root_item_id)

    def print_item_tree(self, item, depth = 0):
        if item in self.items:
            indent = ''
            for i in range(0, depth):
                indent = indent + ';'
            print(indent + self.items[item]['name'])

            if self.items[item]['type'] == 'Category':
                if 'categories' in self.items[item]:
                    for c in self.items[item]['categories']:
                        self.print_item_tree(c, depth + 1)
                elif 'products' in self.items[item]:
                    for brand in self.items[item]['products']:
                        print("{0};{1}".format(indent, brand))
                        for product in self.items[item]['products'][brand]:
                            print("{0};;{1} - {2}".format(indent, product['id'], product['name']))