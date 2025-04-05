class NullPointerException(Exception):
    def __init__(self, message="Null value encountered"):
        self.message = message
        super().__init__(self.message)