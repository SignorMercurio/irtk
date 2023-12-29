import util

from config import config

custom_log_path = config['log']['custom_log_path']

def recon():
    output = "\n## Web 日志信息\n"

    output += f"#### Nginx\n{get_nginx()}\n"
    output += f"#### Apache\n{get_apache()}\n"
    output += f"#### {custom_log_path}\n{get_custom()}\n"

    return output

def get_nginx():
    command = "netstat -anplt | grep nginx"
    result = util.exec_cmd(command)
    if result == "":
        return "Nginx is not running"
    
    command = "cat /var/log/nginx/access.log"
    return util.to_code(util.exec_cmd(command))

def get_apache():
    if util.get_os_release() == 'CentOS':
        program_name = "httpd"
        log_path = "/var/log/httpd/access_log"
    else:
        program_name = "apache2"
        log_path = "/var/log/apache2/access.log"

    command = f"netstat -anplt | grep {program_name}"
    result = util.exec_cmd(command)
    if result == "":
            return "Apache server is not running"
    
    command = f"cat {log_path}"
    return util.to_code(util.exec_cmd(command))

def get_custom():
    command = f"cat {custom_log_path}"
    return util.to_code(util.exec_cmd(command))
