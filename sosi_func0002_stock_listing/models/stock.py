class stock(object):
    """
        Class that represents the 'stock' data model for simple info like 'detail', 'company name' and 'stock code'
    """

    code: str()
    company: str()
    detail: str()
    date_time_operation: str()

    def __init__(self, code, company, detail, dt_operation):
        """
            Class initializer

            Args:
                code = Stock Code
                company = Company name
                detail = Extra details that may support the operation
                dt_operation = Date & Time from crawling operation
        """
        self.code = code
        self.company = company
        self.detail = detail
        self.date_time_operation = dt_operation
        pass
    pass