import os
import json
import tarfile
from productscraper.configuration import Configuration

class ProductsDumper:
    def __init__(self, config: Configuration, items: dict):
        self.config = config
        self.items = items

    def dump(self):
        self.save_as_json()
        self.save_as_csv()

    def save_as_json(self):
        if len(self.config.to_json_file):
            with open(self.config.to_json_file, "w") as f:
                f.write(json.dumps(self.items))

            with tarfile.open(self.config.to_json_file + ".tar.bz2", "w:bz2") as tar:
                tar.add(self.config.to_json_file)

            os.remove(self.config.to_json_file) # cleanup

    def save_as_csv(self):
        if len(self.config.to_csv_file):
            with open('unsorted.csv', "w") as f:
                self.dfs(f, self.items, self.config.root_item['id'])

            with open(self.config.to_csv_file, "w") as f_sorted, open('unsorted.csv', "r") as f_unsorted:
                for l in sorted(f_unsorted.readlines()):
                    f_sorted.write(l)
                
            with tarfile.open(self.config.to_csv_file + ".tar.bz2", "w:bz2") as tar:
                tar.add(self.config.to_csv_file)

            # cleanup
            os.remove(self.config.to_csv_file)
            os.remove('unsorted.csv')

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
