import json
import os


class FileManager:
    def __init__(self, config_path):
        self.config_path = config_path + '/config.json'
        self.config = self.load_config()

        self.local_path = config_path + '/__local__'

    def load_config(self):
        with open(self.config_path, 'r') as config:
            return json.load(config)

    def get_config(self, item, reload=False):
        if reload:
            self.config = self.load_config()

        if item not in self.config.keys():
            return None
        return self.config[item]

    def read_local(self, file_name):
        path = os.path.join(self.local_path, file_name)
        mode = 'r' if os.path.isfile(path) else 'w+'

        with open(path, mode) as local:
            return local.read()

    def write_local(self, file_name, contents, append=True):
        path = os.path.join(self.local_path, file_name)
        mode = 'a+' if append else 'w+'

        with open(path, mode) as local:
            local.write(contents)
