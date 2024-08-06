'''
run.py

Usage: $ python run.py
'''

from rad.app import create_app
app = create_app( environment = 'DEV')

@app.route("/")
def hello():
    return "Hello! This is the skeletion!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)    
