import json
from quiz import addtobase
import psycopg2
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route('/questions', methods = ['POST'])
def update_list():
    new_one = request.json
    opt = new_one["questions_num"]
    pak = addtobase(num = opt)
    return jsonify(pak)

app.run(
    host="0.0.0.0"
    , port=4999
    , debug=True
)

