import util

def recon():
    output = "\n## 网络信息\n"

    output += f"#### TCP 端口监听\n{get_listen_port()}\n"
    output += f"#### 网络连接\n{get_link()}\n"
    output += f"#### DNS 服务器\n{get_dns_server()}\n"
    output += f"#### /etc/hosts\n{get_etc_hosts()}\n"

    return output

def get_etc_hosts():
    command = "cat /etc/hosts"
    return util.to_code(util.exec_cmd(command))

def get_listen_port():
    command = "netstat -plnt | ag 'tcp.*' --no-color"
    return util.to_code(util.exec_cmd(command))

def get_link():
    command = "netstat -plant | ag ESTAB --no-color"
    return util.to_code(util.exec_cmd(command))

def get_dns_server():
    command = "ag -o '\d+\.\d+\.\d+\.\d+' --nocolor </etc/resolv.conf"
    return util.to_code(util.exec_cmd(command))

