""" rad.app.py """
from flask import Flask

# import the blueprints
from rad.auth import routes as Auth
from rad.doc  import routes as Doc
from rad.home import routes as Home


'''
Creates a new Flask application instance.

Params:
    environment : Envr configuration value, Default is 'DEV'        

Returns:
    app: A Flask app instance.
'''
def create_app ( environment ):
    app = Flask(__name__)

    # Configs
    ## Housekeeping : use config.py
    if environment == 'DEV':
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = 'DEV<KEY>'
    elif environment == 'PRD':
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'PRD<KEY>'
    else:
        raise ValueError('Invalid environment') 
    
    # Databases
    ## Housekeeping : Connections & Models ...
    
    # Routes
    ## Register imported Blueprints / Controllers
    app.register_blueprint(Home.bp_home, url_prefix='/')
    app.register_blueprint(Auth.bp_auth, url_prefix='/auth/')
    app.register_blueprint(Doc.bp_doc,   url_prefix='/doc')

    return app