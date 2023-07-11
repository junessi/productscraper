import json
from productscraper import utils

class Configuration:
    def __init__(self,
                 spider_name: str = '',
                 root_item: dict = {},
                 dump_directory: str = '',
                 to_json_file: str = '',
                 to_csv_file: str = ''):
        self._spider_name = spider_name
        self._root_item = root_item
        self._dump_directory = dump_directory
        self._to_json_file = to_json_file
        self._to_csv_file = to_csv_file

    @property
    def spider_name(self):
        return self._spider_name

    @spider_name.setter
    def spider_name(self, name):
        self._spider_name = name

    @property
    def root_item(self):
        return self._root_item

    @root_item.setter
    def root_item(self, root_item):
        self._root_item = root_item

    @property
    def to_json_file(self):
        return self._to_json_file

    @to_json_file.setter
    def to_json_file(self, filename):
        self._to_json_file = filename

    @property
    def to_csv_file(self):
        return self._to_csv_file

    @to_csv_file.setter
    def to_csv_file(self, filename):
        self._to_csv_file = filename

    @property
    def dump_directory(self):
        return self._dump_directory

    @dump_directory.setter
    def dump_directory(self, dir_path):
        self._dump_directory = dir_path


def load_config(spider_name):
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            spider_config = None
            for spider in config['spiders']:
                if spider['name'] == spider_name:
                    spider_config = spider
                    break

            if spider_config == None:
                raise Exception("spider {0} is undefined")

            c = Configuration()
            c.spider_name = spider_name
            c.root_item = spider_config['root_item']
            c.dump_directory = config['dump_directory']
            if spider_config['save_to_json_file']:
                c.to_json_file = "{0}_{1}.json".format(spider_name, utils.get_yyyymmdd())
            if spider_config['save_to_csv_file']:
                c.to_csv_file = "{0}_{1}.csv".format(spider_name, utils.get_yyyymmdd())

            return c
    except Exception as e:
        print("Failed to load config: {0}".format(e))

    return None