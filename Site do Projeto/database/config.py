class Config:
    SECRET_KEY = "superdificil"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/databasepi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False