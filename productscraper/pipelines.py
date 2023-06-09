from datetime import datetime
import threading
import json
import copy

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
        with open("kramp.json", "w") as f:
            f.write(json.dumps(self.items))
        self.save_as_csv(self.root_item_id)


    def save_as_csv(self, root_item_id):
        with open('kramp123.csv', "w") as f:
            self.dfs(f, self.items, root_item_id)

    def dfs(self, f_handle, items, item_id, path = []):
        try:
            path.append(items[item_id]['name'])
            if len(items[item_id]["categories"]):
                for child_id in items[item_id]["categories"]:
                    self.dfs(f_handle, items, child_id, path)

            else:
                for p in items[item_id]["products"]:
                    line = ""
                    if len(path):
                        line = ";".join(path) + ";"

                    line += "{0};{1};{2}".format(p['brand'], p['id'], p['name'])
                    f_handle.write("{0}\n".format(line))
        except:
            print("unable to process this item:")
            print(items[item_id])

        path.pop()
