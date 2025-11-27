import os

class Config:
    """Configurações padrão"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fittrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'sua-chave-secreta-mudable-em-producao'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-super-secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///fittrack.db'
    )

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
