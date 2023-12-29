import util

def recon():
    output = "\n## SSH 信息\n"

    output += f"#### SSH 暴力破解\n{get_bruteforce()}\n"
    output += f"#### 最近成功登录情况\n{get_last_login()}\n"
    output += f"#### SSH 配置信息\n{get_config()}\n"
    output += f"#### SSH 公钥信息\n{get_keys()}\n"
    output += f"#### SSH 公钥状态\n{util.get_file_stat('/root/.ssh/authorized_keys')}\n"
    output += f"#### sshd 配置信息\n{get_sshd_config()}\n"
    output += f"#### SSH 软链接后门\n{get_ln_backdoor()}\n"
    output += f"#### SSH inetd 后门\n{get_inetd_backdoor()}\n"
    output += f"#### SSH xinetd 后门\n{get_xinetd_backdoor()}\n"

    return output

def get_bruteforce():
    command = "ag -a 'authentication failure' /var/log/secure* /var/log/auth.* | awk '{print $14}' | awk -F '=' '{print $2}' | ag '\d+\.\d+\.\d+\.\d+' | sort | uniq -c | sort -nr | head -n 25"
    return util.to_code(util.exec_cmd(command))

def get_last_login():
    command = "last"
    return util.to_code(util.exec_cmd(command))

def get_config():
    command = "cat ~/.ssh/config"
    return util.to_code(util.exec_cmd(command))

def get_keys():
    command = "cat ~/.ssh/authorized_keys"
    return util.to_code(util.exec_cmd(command))

def get_sshd_config():
    command = "cat /etc/ssh/sshd_config | grep -vE '#|^$'"
    return util.to_code(util.exec_cmd(command))

def get_ln_backdoor():
    command = "ps -ef | ag '\s+\-oport=\d+' --no-color"
    return util.to_code(util.exec_cmd(command))

def get_inetd_backdoor():
    command = "cat /etc/inetd.conf | grep -vE '#|^$'"
    return util.to_code(util.exec_cmd(command))

def get_xinetd_backdoor():
    command = "cat /etc/xinetd.conf | grep -vE '#|^$'"
    return util.to_code(util.exec_cmd(command))
