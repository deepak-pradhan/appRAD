""" rad.doc.routes.py """
from flask import render_template

# from rad.doc import bp_doc
from flask import Blueprint
bp_doc = Blueprint('bp_doc', __name__, template_folder='views') 

@bp_doc.route('/')
@bp_doc.route('/index')
def doc():
    return render_template('index.jinja'
            , title='Doc - Index'
    )

@bp_doc.route('/doc/<file>')
def render_md(file):
    return render_template('login.j2'
            , title='Doc - md page'
        )
