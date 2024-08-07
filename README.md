# appRAD 


## Pre-requisites

### Git & GH basic familarization  
---  
24.08.05:    

```yaml
Created Repo (appRAD)
git clone Repo: > Local copy

Browser change ReadMe.md 
: Local Un-sycnd
git fetch + git pull: > Local Syncd

VCS change ReadMe.md 
: Repo Un-sycnd
GH Desktop : Select changes
, Enter message/ description
, Commit to patch-1 
, Push origin

```

### Install Flask   
---   
24.08.05   

```bash
$ cd appRAD

$ python3 -m venv .venv
$ . .venv/bin/activate

$ (.venv) pip install --upgrade pip
$ (.venv) pip install Flask
```

## Skeleton-bare   
---   
24.08.05   

<pre>
/appRAD
├── run.py
├── /rad
│   ├── app.py
</pre>


```py
""" rad.app.py """
from flask import Flask

# Creates app 
# returns app
def create_app ( environment ):
    app = Flask(__name__)
    return app
```

```py
""" run.py
Usage: $ python run.py
"""
# Imports app
from rad.app import create_app
app = create_app( environment = 'DEV')

# Routes
@app.route("/")
def hello():
    return "Hello! This is the skeletion-bare!"

# Starts app
if __name__ == "__main__":
    app.run(port=5000, debug=True)   
```    

[Test: http://127.0.0.1:5000/](http://127.0.0.1:5000/)   
o/p: "Hello! This is the skeletion!"

Commit!


## Skeleton-Baby-V.00   
---   
24.08.06   


```gherkin

UC-fr.01: Test routes from run.py
Scenario: Routes - Basics

Given that my routes are:
  index, about, contact, doc,register, login, logout, error401, error402, error403

When I organize them into groups (for Modules / BluePrints)

Then I should see 4 Groups/ Modules:
    | Module    | routes / BluePints           |
    | --------- | ---------------------------- |
    | Home      | index, about, contact        |
    | Auth      | register, login, logout      |
    | Errors    | error401, error402, error403 |
    | Doc       | doc                          |
```

<pre>
/appRAD
├── run.py
├── /rad
│   ├── app.py
</pre>


```py
""" rad.app.py """
from flask import Flask
def create_app ( environment ):
    app = Flask(__name__)
    return app
```

```py
""" run.py
Usage: $ python run.py
"""
from rad.app import create_app
app = create_app( environment = 'DEV')

# Routes
'''
@Uses: url_for Helper
'''
@app.route("/")
@app.route("/index")
def hello():
    return f'''
    <pre>
    index.html
    
    Group 1: URLs for Home routes / bp Home
    <a href={url_for('index')}>Index</a> 
    <a href={url_for('about')}>about</a> 
    <a href={url_for('doc')}>doc</a>

    Group 2: URLs for Auth routes / bp Auth:
    <a href={url_for('register')}>register</a>
    <a href={url_for('login')}>login</a> 
    ...

    Group 3: URLs for Errors routes / bp Errors:
    <a href={url_for('errors/4xx/error_404')}>404</a>
    ...
    </pre>
    '''


# Starts app
if __name__ == "__main__":
    app.run(port=5000, debug=True)   
```    

[Open: http://127.0.0.1:5000/](http://127.0.0.1:5000/)  
Test link from index to new-tab 
o/p: "Hello! This is the skeletion!"

Commit!