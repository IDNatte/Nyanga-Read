class UAError(Exception):
    """
    User Agent Exception error
    """

    def __init__(self, name, description, code):
        self.name = name
        self.description = description
        self.code = code


class CSRFError(Exception):
    """
    CSRF Exception error
    """

    def __init__(self, name, description, code):
        self.name = name
        self.description = description
        self.code = code
