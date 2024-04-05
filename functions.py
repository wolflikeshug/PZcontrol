import subprocess
import os

service_path = "./service.sh"
log_path = "logs/"

def start_service_with_nohup():
    try:
        log_file_name = f"service.log"
        
        # 构建包含时间戳的日志文件名的命令
        command = f"mv *.log {log_path}; rm service.pid; nohup {service_path} > {log_file_name} 2>&1 & echo $!"
        
        # 执行命令，使用shell=True
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # 读取输出（即后台进程的PID）
        pid = process.stdout.readline().strip()
        with open("service.pid", "w+") as pid_file:
            pid_file.write(pid)
        return 0
    except Exception as e:
        return str(e)

def stop_service_with_pid():
    try:
        with open("service.pid", "r") as pid_file:
            pid = pid_file.read().strip()
            command = f"kill -9 {pid}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return 0
    except Exception as e:
        return str(e)

def restart_service():
    stop_service_with_pid()
    return start_service_with_nohup()

def is_process_running():
    try:
        with open("service.pid", "r") as pid_file:
            pid = pid_file.read().strip()
            # os.kill在这里不会真的杀掉进程；它只是发送一个无害的信号来检查进程是否存在
            os.kill(pid, 0)
    except OSError:
        # 如果进程不存在，将抛出OSError异常
        return False
    else:
        # 如果没有异常，说明进程存在
        return True
    
def read_log_file():
    try:
        with open("service.log", "r") as log_file:
            return log_file.read()
    except Exception as e:
        return str(e)