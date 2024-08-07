'''
run.py
Usage: $ python run.py
'''
from rad.app import create_app
from flask import url_for

app = create_app( environment = 'DEV')

# Home routes/controller
@app.route("/")
@app.route("/index")
def index():
    return f'''
    <pre>
    index.html
    
    Group 1: URLs for Home routes / bp Home
    <a href={url_for('index')}>Index</a> 
    <a href={url_for('about')}>about</a> 
    <a href={url_for('contact')}>contact</a>
    <a href={url_for('doc')}>doc</a>

    Group 2: URLs for Auth routes / bp Auth:
    <a href="{url_for('register')}">register</a>
    <a href={url_for('login')}>login</a> 
    <a href={url_for('logout')}>logout</a> 
    ...

    Group 3: URLs for Errors routes / bp Errors:
    <a href={url_for('error_403')}>403</a>
    <a href={url_for('error_404')}>404</a>
    ...
    </pre>
    '''

@app.route('/about')
def about():
    return """Okay, about!"""

@app.route("/contact")
def contact():
    return """Okay, contacted"""

# Routes/Controllers for Authentication
@app.route('/auth/register')
def register():
    return """registered, please verify your email address"""

@app.route("/auth/verify-email")
def verify_email():
    return """verified email-registration"""

@app.route('/auth/login')
def login():
    return """logged in"""

@app.route("/auth/logout")
def logout():
    return """logged out"""

@app.route("/auth/forgot-password")
def forgot_password():
    return """forgot password? email has been sent to your email address"""

@app.route('/auth/reset-password')
def reset_password():
    return """reseted password"""


# Routes/Controllers for User
@app.route("/user")
def user():
    return """user"""

@app.route('/admin')
def admin():
    return """admin"""

@app.route("/role")
def role():
    return """role"""

@app.route("/profile")
def profile():
    return """profile"""


# Routes/Controllers for ErrorS
## 1xx : Informational (e.g., 100, 101)
## 2xx : Success (e.g., 200, 201)
## 3xx : Redirection (e.g., 300, 301)

## 4xx : Client Error (e.g., 400, 401, 403, 404)
@app.route('/400')
def error_400():
    return """error 400"""

@app.route('/401')
def error_401():
    return """error 401"""

@app.route('/error_403')
def error_403():
    return """error 403"""

@app.route('/error_404')
def error_404():
    return """error 404"""

## 5xx : Server Error (e.g., 500, 501, 502, 503)
@app.route('/500')
def error_500():
    return """error 500"""

# Routes/Controllers for Documentation
@app.route('/doc')
def doc():
    return """doc"""

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=5000
    )    
