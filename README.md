# appRAD


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



### Skeleton   
---   
24.08.05   

```py
''' rad.app.py
'''

from flask import Flask

def create_app ( environment ):
    app = Flask(__name__)
    return app
```

```py
''' run.py
Usage: $ python run.py
'''

from rad.app import create_app
app = create_app( environment = 'DEV')

@app.route("/")
def hello():
    return "Hello! This is the skeletion!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)   
```    

[Test: http://127.0.0.1:5000/](http://127.0.0.1:5000/)