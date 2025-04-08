import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'mi_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sales_management.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
