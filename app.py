'''
app.py

Flask server for handling OAuth2 requests

@ethanpinter
'''

# imports 
from flask import Flask, request
import logger
from threading import Thread

app = Flask(__name__)

@app.get("/callback")
def callback():
    code = request.args.get("code")
    return code

if __name__ == '__main__':
    app.wsgi_app = logger.Logger(app.wsgi_app)
    Thread(target=app.run(port=3000)).run()
