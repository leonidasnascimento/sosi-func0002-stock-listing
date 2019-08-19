class stock():
    """
        Class that represents the 'stock' data model for simple info like 'detail', 'company name' and 'stock code'
    """

    code: str()
    company: str()
    detail: str()

    def __init__(self):
        self.code = ''
        self.company = ''
        self.detail = ''
        pass
    pass