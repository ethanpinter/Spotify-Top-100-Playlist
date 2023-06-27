
from flask import Flask, request
import logger

app = Flask(__name__)

@app.get("/callback")
def callback():
    code = request.args.get("code")
    return code
'''
@app.get("/token")
def get_token():
    return None # TO-DO
'''
if __name__ == '__main__':
    app.wsgi_app = logger.Logger(app.wsgi_app)
    app.run(port=3000)
