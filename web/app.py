import os, io, json
import waitress
from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin

@app.route('/', methods=['GET'])
def home():
    return "hello world"