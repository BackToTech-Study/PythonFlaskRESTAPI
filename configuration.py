class Configuration:
    def __init__(self):
        self.DEBUG = False
        self.ENV = 'production'
        self.SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:secret_key@localhost:5432/demo_db'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
