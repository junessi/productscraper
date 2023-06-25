class Configuration:
    def __init__(self, root_item: dict,
                 to_json_file: str = '',
                 to_csv_file: str = ''):
        self._root_item = root_item
        self._to_json_file = to_json_file
        self._to_csv_file = to_csv_file

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

