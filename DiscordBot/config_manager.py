import json


class ConfigManager:
    def __init__(self, config_path):
        self.path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.path, 'r') as config:
            return json.load(config)

    def get(self, item, reload=False):
        if reload:
            self.config = self.load_config()

        if item not in self.config.keys():
            return None
        return self.config[item]
