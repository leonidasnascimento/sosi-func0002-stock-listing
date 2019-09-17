from configuration_manager.base_classes import base_config_manager

class reader(base_config_manager.base_config_manager):
    '''
        Class responsible tha encapsulates the methods to read a given JSON file
    '''
    # Class initializer
    def __init__(self, path, node):
        super().__init__(path, node)
        
    # Gets the value from a given key
    def get_value(self, key, default_value=None):
        '''
            Read a key from the JSON file and returns a value

            Args:
                key = Key that is supposed to be read
                default_value = The default value returned in case 'key' not found
        '''
        value = self.configuration.get_value(key)
        
        if value is None:
            return default_value

        return value 
