class config():
    full_path: str = None
    values: {} = None

    # Class initializer
    def __init__(self, path: ""):
        self.full_path = path
        self.values = {}

    def add_value(self, key, value):
        self.values[key] = value

    def remove_value(self, key, value):
        self.values.pop(key, value)

    def get_value(self, key):
        if self.values:
            return self.values.get(key, None)
        return None
