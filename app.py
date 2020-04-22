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




#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 



app = Flask(__name__)






@app.route('/bb')
def hello_world():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <video id="video" width="640" height="480" autoplay></video>
    <button id="snap">Snap Photo</button>
    <canvas id="canvas" width="640" height="480"></canvas>
    </body>
    <script>

    var video = document.getElementById('video');
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            //video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();
        });
    }

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');

    // Trigger photo take
    document.getElementById("snap").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
        var dataURL = canvas.toDataURL();
        console.log(dataURL);
    $.ajax({
  type: "POST",
  url: "/submit",
  data:{
    imageBase64: dataURL
  }
}).done(function() {
  console.log('sent');
});


    });



</script>
</html>
    """

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        imgData = base64.b64decode(request.form['imgdata'].replace('data:image/png;base64,', ''))
        finename=str(int(round(time.time() * 1000))) + '.jpg'
        file = open(finename, 'wb')
        file.write(imgData)
        file.close()
        return json.dumps(realtime.hh(finename),ensure_ascii=False)
    else:
         return render_template("test3.html")


@app.route('/hook', methods=['POST'])
def disp_pic():
    data = request.data
    encoded_data = data.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




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

