import paramiko
import subprocess

from config import config

local = True if config['mode'] == 'local' else False
client = paramiko.SSHClient()

def connect_to_host(ssh_info):
    trans = paramiko.Transport((ssh_info['host'], ssh_info['port']))
    trans.connect(username=ssh_info['username'], password=ssh_info['password'])

    client._transport = trans
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def exec_cmd(command):
    if local:
        try:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).strip().decode('utf-8')
        except subprocess.CalledProcessError as e:
            result = e.output.strip().decode('utf-8')
    else:
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().strip().decode('utf-8')
        if len(result) == 0:
            result = stderr.read().strip().decode('utf-8')
        stdin.close()
    return result

def to_code(string):
    return "```\n" + string + "\n```"

def get_os_release():
    command = 'source /etc/os-release && echo $ID'
    result = exec_cmd(command)

    centos = ['centos', 'rhel', 'rhel fedora']
    debian = ['debian', 'ubuntu', 'devuan']

    if result in centos:
        return 'CentOS'
    elif result in debian:
        return 'Debian'
    else:
        return 'Unknown'

def install_tool(os_release, tool, yum_pkg, apt_pkg):
    if os_release == 'CentOS':
        output = exec_cmd(f"yum install -y {yum_pkg}")
    else:
        output = exec_cmd(f"apt install -y {apt_pkg}")
    if 'already' in output:
        return
    print(output)

def get_file_stat(target_file):
    command = f"stat {target_file} | ag 'Access|Modify|Change' --nocolor"
    return to_code(exec_cmd(command))
