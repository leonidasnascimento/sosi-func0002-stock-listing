import json
from abc import ABC
from configuration_manager.domain.config import config

class base_config_manager(ABC):
    configuration: config = None

    def __init__(self, path, node):
        self.configuration = config(path)
    
        val = json.loads(open(self.configuration.full_path).read())
        val_aux = {}

        if str(node).__len__() > 0:
            val_aux = val[node]
        else:
            val_aux = val

        if val_aux is not None:
            for key, value in val_aux.items():
                self.configuration.add_value(key, value)