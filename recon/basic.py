import util

def recon():
    output = '## 基础信息\n'

    os_release = util.get_os_release()
    output += f'- OS 发行版：{os_release}\n'

    util.install_tool(os_release, 'ag', 'the_silver_searcher', 'silversearcher-ag')
    util.install_tool(os_release, 'lsof', 'lsof', 'lsof')
    print('[+] 工具安装完成')

    ip_addr = get_ip_addr().split('\n')
    output += f'- IP 地址：{" ".join(ip_addr)}\n'
    hostname = get_hostname()
    output += f'- 主机名：{hostname}\n'
    output += f'#### CPU 使用率\n{get_cpu_stat()}\n'
    output += f'#### 内存使用率\n{get_mem_stat()}\n'
    output += f'#### 磁盘空间\n{get_disk_stat()}\n'

    return output, os_release, ip_addr[0], hostname

def get_ip_addr():
    command = "ifconfig | ag -o '(?<=inet |inet addr:)\d+\.\d+\.\d+\.\d+' | ag -v '127.0.0.1'"
    return util.exec_cmd(command)

def get_hostname():
    command = "hostname"
    return util.exec_cmd(command)

def get_cpu_stat():
    command = """
awk '$0 ~/cpu[0-9]/' /proc/stat 2>/dev/null | while read line; do
    echo "$line" | awk '{total=$2+$3+$4+$5+$6+$7+$8;free=$5;\
        print$1" Free "free/total*100"%",\
        "Used " (total-free)/total*100"%"}'

    done
    """
    return util.to_code(util.exec_cmd(command))

def get_mem_stat():
    command = "free -mh"
    return util.to_code(" "*14 + util.exec_cmd(command))

def get_disk_stat():
    command = "df -mh"
    return util.to_code(util.exec_cmd(command))
