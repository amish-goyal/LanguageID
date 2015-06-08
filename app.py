"""
This script uses the Flask module to expose the LanguageID functionality
through a RESTful API

Sample Call:
curl -i -H "Content-Type: application/json" -X POST -d '{"text":"test sentence"}' http://localhost:5000/lang_id
"""


#!flask/bin/python
from flask import Flask, jsonify, request
from detectLanguage import *


app = Flask(__name__)


@app.route('/lang_id', methods=['POST'])
def identifyLanguage():
    if not request.json or not 'text' in request.json:
        abort(400)
    ID = getLangID(request.json['text'])
    return jsonify({'lang': ID}), 201


if __name__ == '__main__':
    app.run(debug=True)