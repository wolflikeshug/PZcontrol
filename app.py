from flask import Flask, render_template, redirect, url_for
from functions import *

app = Flask(__name__)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 功能页面路由
@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/start_service')
def start_service():
    if is_process_running():
        return "服务器已经在运行！"
    else:
        return start_service_with_nohup()

@app.route('/stop_service')
def stop_service():
    if is_process_running():
        return stop_service_with_pid()
    else:    
        return "服务器已经停止！"

@app.route('/restart_service')
def commando():
    if is_process_running():
        return restart_service()
    else:
        return start_service_with_nohup()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1145, debug=True)