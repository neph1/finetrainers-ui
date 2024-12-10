from typing import OrderedDict


class Config:

    def __init__(self):
        self.config = OrderedDict()

    def set(self, key: str, value, context: str = ''):
        self.config[(context + '_' + key) if context else key] = value

    def remove(self, key: str, context: str = ''):
        self.config[(context + '_' + key) if context else key] = None

    def get(self, key: str, context: str = ''):
        return self.config.get((context + '_' + key) if context else key)
    
    def get_cogvideox_factory_path(self) -> str:
        return self.config.get('path_to_cogvideox_factory')
    
    def get_all(self) -> OrderedDict.items:
        return self.config.items()
    

global_config = Config()