from configuration import Configuration


class TestConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'development'
