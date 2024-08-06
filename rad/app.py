'''rad.app.py
'''
from flask import Flask


def create_app ( environment ):
    app = Flask(__name__)

    if environment == 'DEV':
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = 'DEV<KEY>'
    elif environment == 'PRD':
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'PRD<KEY>'
    else:
        raise ValueError('Invalid environment') 

    return app