""" rad.auth.routes.py """
from flask import render_template
from rad.auth import bp_auth

@bp_auth.route('/')
@bp_auth.route('/index')
def index():
    return render_template('index.jinja'
            , title='Auth - Index'
    )

@bp_auth.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.jinja'
            , title='Register'
    )

@bp_auth.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.j2'
            , title='Login'
        )

@bp_auth.route('/logout', methods=['GET','POST'])
def logout():
    pass