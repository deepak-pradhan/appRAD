""" 
rad.home.routes.py 
"""
from flask import Blueprint, render_template
bp_home = Blueprint('bp_home', __name__, template_folder='views') 

@bp_home.route('/')
@bp_home.route('/index')
def index():
    return render_template('index.jinja', title='Home')

@bp_home.route('/about')
def about():
    return render_template('about.jinja', title= 'About')

@bp_home.route('/contact')
def contact():
    return render_template('contact.jinja', title='Contact')