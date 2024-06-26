import subprocess
import os
import glob

from datetime import datetime, timedelta, timezone

service_path = "/home/ubuntu/Steam/steamapps/common/Project\ Zomboid\ Dedicated\ Server/start-server.sh -servername ponyland "
log_path = "/home/ubuntu/ProjectZomboid_logs/"

def start_service_with_nohup():
    try:
        # 创建东八区时间对象
        tz_eastern_eight = timezone(timedelta(hours=8))
        
        # 获取当前东八区时间，并格式化为字符串，用作文件名
        # 例如：2024-04-05_12-00-00
        current_time_str = datetime.now(tz_eastern_eight).strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"service_{current_time_str}.log"
        
        # 构建包含时间戳的日志文件名的命令
        command = f"mv /tmp/pz/*.log {log_path}; rm /tmp/pz/service.pid; cd /home/ubuntu/pz && nohup {service_path} > /tmp/pz/{log_file_name} 2>&1 & echo $!"
        
        # 执行命令，使用shell=True
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return "服务器启动成功"
    except Exception as e:
        return str(e)

def stop_service_with_pid():
    """Stop the ProjectZomboid64 service."""
    os.system("pkill -f ProjectZomboid64")
    return "服务已停止。"

def restart_service():
    stop_service_with_pid()
    return start_service_with_nohup()

def is_process_running():
    """Check if ProjectZomboid64 is running."""
    try:
        # This command counts the number of instances of ProjectZomboid64 running
        output = subprocess.check_output(["pgrep", "-f", "ProjectZomboid64"]).decode().strip()
        return bool(output)  # True if output is not empty, meaning the process is running
    except subprocess.CalledProcessError:
        return False
    
import glob

def read_log_file():
    try:
        file_list = glob.glob('/tmp/pz/*log')

        # 检查是否有匹配的文件
        if file_list:
            # 假设只有一个匹配的文件，直接取最新的一个
            file_path = file_list[-1]
            
            # 打开文件并读取最后100行内容
            with open(file_path, 'r') as file:
                lines = file.readlines()  # 读取所有行
                last_100_lines = lines[-100:]  # 获取最后100行
                
            # 将最后100行内容合并为单一字符串返回
            content = ''.join(last_100_lines)
            return content
        else:
            return "未找到匹配的文件。"
    except Exception as e:
        return str(e)
