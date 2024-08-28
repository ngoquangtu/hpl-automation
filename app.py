from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask_cors import CORS
from flask import Flask,jsonify,render_template,request,send_file
import os
import logging
import time
import threading
import uuid

app=Flask(__name__)
CORS(app)

UPLOAD_FOLDER='uploads'
RESULTS_FOLDER='results'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['RESULTS_FOLDER']=RESULTS_FOLDER
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(RESULTS_FOLDER,exist_ok=True)


#config logging 

logging.basicConfig(level=logging.INFO)

def attach_to_chrome():
    # Thiết lập các tùy chọn cho Chrome
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Khởi tạo trình điều khiển cho Chrome
    driver = webdriver.Chrome(options=options)

    try:
        # Truy cập trang Amazon
        driver.get('https://www.amazon.com')

        # Thực hiện các hành động khác nếu cần
        # ...
    finally:
        # Không đóng trình duyệt, chỉ tắt kết nối driver
        # driver.quit()
        pass

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload',methods=['POST'])
def upload_file():
    file=request.files.get('file')
    if file:
        file_id=str(uuid.uuid4())
        file_path=os.path.join(app.config['UPLOAD_FOLDER'],file_id+'.xlsx')
        file.save(file_path)
        return jsonify({"status":"success","file_id": file_id})
    else:
        return jsonify({"status":"error","message":"Vui lòng tải file lên!!!"})
    
# dowload file 

@app.route('/download/<file_id>')
def download_results(file_id):
    output_file_name=file_id+'.xlsx'
    output_file_path=os.path.join(app.config['UPLOAD_FOLDER'],output_file_name)
    if os.path.exists(output_file_path):
        return send_file(output_file_path,as_attachment=True)
    return "Không tìm thấy file tải xuống mất rồi!! Vui lòng kiểm tra lại !!",404
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/track')
def tracking(file_id):
    file_id=request.form