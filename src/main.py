"""Main program to run Flask App. (Entry point)"""
from __init__ import create_app
from os import environ, path
from dotenv import load_dotenv

# get .env 
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(path.dirname(basedir), ".env"))

# get Flask host and port
FLASK_RUN_HOST = environ.get("FLASK_RUN_HOST")
FLASK_RUN_PORT = environ.get("FLASK_RUN_PORT")

# create Flask application 
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)