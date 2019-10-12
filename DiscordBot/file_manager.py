import json
import os


class FileManager:
    def __init__(self, config_path):
        self.config_path = config_path + '/config.json'
        self.config = self.load_config()

        self.local_path = config_path + self.get_config('settings')['local_path']

    def load_config(self):
        with open(self.config_path, 'r') as config:
            return json.load(config)

    def get_config(self, item, reload=False):
        if reload:
            self.config = self.load_config()

        if item not in self.config.keys():
            return None
        return self.config[item]

    def get_local(self, file_name):
        path = os.path.join(self.local_path, file_name)

        with open(path, 'w+') as local:
            return local.read()
