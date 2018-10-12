from flask import Flask
from datetime import datetime
from app import create_app
import os, re

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app('development')

if __name__ == '__main__':
    app.run()

"""
@app.route("/")
def home():
    return 'Hello, Flask!'

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A %d %B, %Y at %X")
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, {0}! It's {1}".format(name, formatted_now)
    return content
""" 