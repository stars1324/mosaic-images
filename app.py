import json

import waitress
from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/uploads', methods=['POST'])
@cross_origin()
def uploads():
    # 判断是否有上传图片的参数
    if 'image' not in request.files:
        return json.dumps({"status": 13000, "data": {"content": "參數錯誤1"}})
    file = request.files['image']
    # 判断是否有上传到图片
    if file.filename == '':
        return json.dumps({"status": 13000, "data": {"content": "參數錯誤2"}})

    # todo 实现上传合成功能

if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=5000)