class stock():
    """
        Class that represents the 'stock' data model for simple info like 'detail', 'company name' and 'stock code'
    """

    code: str()
    company: str()
    detail: str()

    def __init__(self, code, company, detail):
        """
            Class initializer

            Args:
                code = Stock Code
                company = Company name
                detail = Extra details that may support the operation
        """
        self.code = code
        self.company = company
        self.detail = detail
        pass
    pass