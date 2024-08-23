from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = os.path.join(basedir, 'Database')
os.makedirs(dbdir, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or "SecretShush"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{os.path.join(dbdir, "app.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config = {
 'development': DevelopmentConfig,
 'testing': TestingConfig,
 'production': ProductionConfig,
 'default': DevelopmentConfig
}
