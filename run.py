'''
run.py
Usage: $ python run.py
'''
from rad.app import create_app

app = create_app( environment = 'DEV')

if __name__ == "__main__":
    app.run(
        port=5000
        , debug = True
    )    
