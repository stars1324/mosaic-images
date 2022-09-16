import os, io, json
import waitress
from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin

from core import Mosaic

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/uploads', methods=['POST'])
def upload():
    file = request.files['image']
    input_file_path = os.path.abspath(os.path.dirname(__file__))
    input_file = os.path.join(input_file_path + '/images', file.filename)
    file.save(input_file)
    mosaic = Mosaic(input_file, os.path.abspath(os.path.dirname(__file__)) + '/images/output.jpg', os.path.abspath(os.path.dirname(__file__)) + '/../bg/')
    mosaic.run()
    return json.dumps({"status": 12000, "data": {"thumb": "%simages/%s" % (request.host_url, "output.jpg")}})


@app.route('/images/<filename>')
@cross_origin()
def image(filename):
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)) + '/images', filename)


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=5000)
