from typing import OrderedDict


class Config:

    def __init__(self):
        self.config = OrderedDict()

    def set(self, key: str, value):
        self.config[key] = value

    def remove(self, key: str):
        self.config[key] = None

    def get(self, key: str):
        return self.config.get(key, None)
    
    def get_cogvideox_factory_path(self) -> str:
        return self.config.get('path_to_cogvideox_factory')
    
    def get_all(self) -> OrderedDict.items:
        return self.config.items()


global_config = Config()