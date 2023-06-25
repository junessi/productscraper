import json
from datetime import datetime
from productscraper.configuration import Configuration
from productscraper import utils

class ProductsDumper:
    def __init__(self, config: Configuration, items: dict):
        self.config = config
        self.items = items
        self.start_time = datetime.now()

    def dump(self):
        end_time = datetime.now()
        print("duration: {0}".format(end_time - self.start_time))
        with open(self.config.to_json_file, "w") as f:
            f.write(json.dumps(self.items))
        self.save_as_csv(self.config.root_item['id'])

    def save_as_csv(self, root_item_id):
        with open(self.config.to_csv_file, "w") as f:
            self.dfs(f, self.items, root_item_id)

    def dfs(self, f_handle, items, item_id, path = []):
        path.append(items[item_id]['name'])

        try:
            if "categories" in items[item_id] and len(items[item_id]["categories"]):
                for child_id in items[item_id]["categories"]:
                    self.dfs(f_handle, items, child_id, path)

            elif "products" in items[item_id] and len(items[item_id]["products"]):
                for p in items[item_id]["products"]:
                    line = ";".join(path) + ";" if len(path) else ""
                    line += "{0};{1};{2}".format(p['brand'], p['id'], p['name'])
                    f_handle.write("{0}\n".format(line))
                    # print("{0} bytes written".format(nbytes))
            else:
                print("skipped item:")
                print(items[item_id])
        except Exception as e:
            print("Exception: {0}".format(e))
            print("Unable to process this item:")
            print(items[item_id])

        path.pop()
