from decouple import config


DATABASE_URI = "mysql+pymysql://root:@localhost/financial_management?unix_socket=/opt/lampp/var/mysql/mysql.sock"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "fdkjshfhjsdfdskfdsfdcbsjdkfdsdf"
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECURITY_PASSWORD_SALT = config(
        "SECURITY_PASSWORD_SALT", default="very-important")
    MAIL_DEFAULT_SENDER = "postmaster@sandbox311bb16fa39d43e48bc850b9e918c351.mailgun.org"
    MAIL_SERVER = "smtp.mailgun.org"
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = "postmaster@sandbox311bb16fa39d43e48bc850b9e918c351.mailgun.org"
    MAIL_PASSWORD = "29e87392d49729dde2990fac8a774422-451410ff-b707a482"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
