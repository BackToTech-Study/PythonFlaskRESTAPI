from configuration import Configuration


class TestConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'development'
        self.SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:secret_key@localhost:5432/demo_db'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
