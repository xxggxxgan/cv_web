from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import sys
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import realtime
import json
from datetime import timedelta
import base64
import numpy as np
import re
from datetime import timedelta
import picadd
import datetime


#材料库中拥有的所有照片的名字
ultList = ['wearing', 'posing', 'young', 'curious', 'shirt', 'smiling', 'hand', 'food', 'holding', 'sitting', 'laptop', 'computer', 'clothing', 'looking', 'indoor', 'glass', 'camera', 'table', 'donut', 'front', 'drinking', 'glasses']

#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) 
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        imgData = base64.b64decode(request.form['imgdata'].replace('data:image/png;base64,', ''))
        #finename=str(int(round(time.time() * 1000))) + '.jpg'
        finename = "newcapture.jpg"
        file = open(finename, 'wb')
        #file = open("newcapture.jpg", 'wb')
        file.write(imgData)
        file.close()
        #result = json.loads(str(json.dumps(realtime.hh("newcapture.jpg"),ensure_ascii=False)))
        result = realtime.hh("newcapture.jpg")
        getTag = result['description']['tags'] 
        print(getTag)
        #return result
        return redirect(url_for('foo'))
    else:
         return render_template("test3.html")


@app.route('/foo')
def foo():
    gender = ''
    basepath = os.path.dirname(__file__)
    result = realtime.hh("newcapture.jpg")
    getTag = result['description']['tags']
    text = result['description']['captions'][0]['text']
    today = str(datetime.datetime.now().strftime('%b %d, %Y'))
    print(text)
    print(today)
    print("all we get is ",getTag)

    # for i in range(len(getTag)):
    #     if getTag[i] == 'boy':
    #         getTag[i] = 'man'
    #     if getTag[i] == 'lady':
    #         getTag[i] = 'woman'
    #     if getTag[i] == 'girl':
    #         getTag[i] = 'woman'
    if 'man' in getTag and 'woman' in getTag:
        h1 = getTag.index('man')
        h2 = getTag.index('woman')
        if(h1<h2):
            gender = 'male'
        else:
            gender = 'female'
    lst3 = [value for value in getTag if value in ultList]
    print("common list we get is ",lst3)
    lst3 = lst3[0:9]
    while len(lst3)<9:
        lst3.append('curious')
    outPut = [name + ".jpg" for name in lst3]
    #print(outPut)
    picadd.image_final(gender,outPut,text,today)
    return render_template("resultt.html", user_image = "./static/images/final.jpg")


@app.route('/a', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        result = json.dumps(realtime.hh("static/images/test.jpg"),ensure_ascii=False)
        print(result)
        return render_template('upload_ok.html',userinput=result,val1=time.time())
    
    return render_template('upload.html')


@app.route('/func', methods=['GET', 'POST'])
def runapp():
    result = json.dumps(realtime.hh("static/images/sbb.png"),ensure_ascii=False)
    return result





if __name__ == "__main__":
    app.run(debug=True)

