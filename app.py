from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/callback", methods=['GET'])
def parse_request():
    data = request.args.get('code') # empty in some cases
    print(data)
    # always need raw data here, not parsed form data
