import os, io, json
import waitress
from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "hello world"


@app.route('/uploads', methods=['POST'])
def upload():
    return "upload"

if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=5000)
