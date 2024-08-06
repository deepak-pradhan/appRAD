from flask import Flask


def create_app ( environment ):
    app = Flask(__name__)
    return app