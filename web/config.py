import os

def config():
    config_dict = {}

    config_dict['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    config_dict['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config_dict['SECRET_KEY'] = 'a really really really really long secret key'
    config_dict['MAIL_SERVER'] = 'smtp.googlemail.com'
    config_dict['MAIL_PORT'] = 587
    config_dict['MAIL_USE_TLS'] = True
    config_dict['MAIL_USERNAME'] = 'youmail@gmail.com'
    config_dict['MAIL_DEFAULT_SENDER'] = 'youmail@gmail.com'
    config_dict['MAIL_PASSWORD'] = 'password'
    config_dict['SUM'] = 0
    config_dict['APP_DIR'] = os.path.abspath(os.path.dirname(__file__))


    return config_dict
