import util

def recon():
    output = "\n## 服务信息\n"

    output += f"#### 用户自定义启动项\n{get_chkconfig()}\n"
    output += f"#### 运行中的服务\n{get_running_service()}\n"
    output += f"#### 最近添加的服务\n{get_recent_service()}\n"
    output += f"#### initd 启动项\n{get_initd()}\n"
    output += f"#### /etc/rc.local 启动项\n{get_rc_local()}\n"

    return output

def get_chkconfig():
    command = "chkconfig --list | ag ':on|启用' --no-color"
    return util.to_code(util.exec_cmd(command))

def get_running_service():
    command = "systemctl list-units --type=service --state=running --no-pager | ag running --no-color | awk '{print $1}' | ag -v 'aegis|aliyun|assistdaemon|atd|auditd|chronyd|crond|dbus|getty|gssproxy|network|polkit|postfix|rpcbind|rsyslog|sshd|systemd|tuned|firewalld|selinux|networkmanager|dnsmasq|avahi-daemon|cups|acpid'"
    return util.to_code(util.exec_cmd(command))

def get_recent_service():
    command = "ls -halt /etc/systemd/system/*.service | ag -v 'dbus-org'"
    return util.to_code(util.exec_cmd(command))

def get_initd():
    command = "ls -halt /etc/rc.d/rc[0-6].d /etc/rc.d/init.d"
    return util.to_code(util.exec_cmd(command))

def get_rc_local():
    command = "cat /etc/rc.local | ag -v '^#'"
    return util.to_code(util.exec_cmd(command))
