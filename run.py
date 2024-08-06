'''
run.py
Usage: $ python run.py
'''
from rad.app import create_app
app = create_app( environment = 'DEV')

@app.route("/")
def hello():
    return """
    <pre>
        WHEN environment = DEV THEN Debug mode is ON
        WHEN environment = PRD THEN Debug mode is OFF
        ELSE ValueError: Invalid environment
    </pre>    
    """

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=5000
    )    
