import util

from config import config

files = config['files']
mtime = files['mtime']
ctime = files['ctime']
large_files_threshold = files['large_files_threshold']

def recon():
    output = "\n## 文件信息\n"

    output += f"#### 临时文件目录\n{get_tmp()}\n"
    output += f"#### SUID\n{get_suid()}\n"
    output += f"#### 被进程锁定的文件\n{get_lsofL1()}\n"
    output += f"#### 可疑历史命令\n{get_susp_bash_history()}\n"
    output += f"#### 传输文件情况\n{get_file_transfer()}\n"

    if files['verbose']:
        output += f"#### {mtime} 天内被修改的文件（mtime）\n{get_recent_modify()}\n"
        output += f"#### {ctime} 天内被修改的文件（ctime）\n{get_recent_change()}\n"
        output += f"#### {large_files_threshold} 以上文件\n{get_large_files()}\n"
        output += f"#### 可疑文件\n{get_susp_files()}\n"

    return output

def get_tmp():
    command = "ls -halt /tmp /var/tmp /dev/shm"
    return util.to_code(util.exec_cmd(command))

def get_suid():
    command = """
    find / ! -path "/proc/*" -perm -004000 -type f | ag -v 'snap|docker|pam_timestamp_check|unix_chkpwd|ping|mount|su|pt_chown|ssh-keysign|at|passwd|chsh|crontab|chfn|usernetctl|staprun|newgrp|chage|dhcp|helper|pkexec|top|Xorg|nvidia-modprobe|quota|login|security_authtrampoline|authopen|traceroute6|traceroute|ps'
    """
    return util.to_code(util.exec_cmd(command))

def get_lsofL1():
    command = "lsof -n +L1"
    return util.to_code(util.exec_cmd(command))

def get_recent_modify():
    command = f'find /etc /bin /lib /sbin /dev /root/ /home /tmp /var /usr ! -path "/var/log*" ! -path "/var/spool/exim4*" ! -path "/var/backups*" -mtime -{mtime} -type f ' + "| ag -v '\.log|cache|vim|/share/|/lib/|.zsh|.gem|\.git|LICENSE|README|/_\w+\.\w+|\blogs\b|elasticsearch|nohup|i18n|/usr/local/aegis|/usr/local/lib64/python' | xargs -i{} ls -halt {}"
    return util.to_code(util.exec_cmd(command))

def get_recent_change():
    command = f'find /etc /bin /lib /sbin /dev /root/ /home /tmp /var /usr ! -path "/var/log*" ! -path "/var/spool/exim4*" ! -path "/var/backups*" -ctime -{ctime} -type f ' + "| ag -v '\.log|cache|vim|/share/|/lib/|.zsh|.gem|\.git|LICENSE|README|/_\w+\.\w+|\blogs\b|elasticsearch|nohup|i18n|/usr/local/aegis|/usr/local/lib64/python' | xargs -i{} ls -halt {}"
    return util.to_code(util.exec_cmd(command))

def get_large_files():
    command = f'find / ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/boot/*" -size +{large_files_threshold} ' + "-exec ls -halt {} + 2>/dev/null | ag '\.gif|\.jpeg|\.jpg|\.png|\.zip|\.tar.gz|\.tgz|\.7z|\.log|\.xz|\.rar|\.bak|\.old|\.sql|\.1|\.txt|\.tar|\.db|/\w+$' --nocolor | ag -v 'ib_logfile|ibd|mysql-bin|mysql-slow|ibdata1'"
    return util.to_code(util.exec_cmd(command))

def get_susp_bash_history():
    command = "cat /root/.bash_history | ag 'tar |zip |rm |wget |curl |chmod |chattr |ssh |scp |useradd |groupadd |userdel | groupdel |rz | sz |whois |sqlmap |nmap |beef |nikto |john |ettercap |backdoor |proxy |msfconsole |msf ' --no-color"
    return util.to_code(util.exec_cmd(command))

def get_susp_files():
    command = """
    find / ! -path "/lib/modules*" ! -path "/usr/src*" ! -path "/snap*" ! -path "/usr/include/*" ! -path "/usr/local/aegis/*" -regextype posix-extended -regex '.*sqlmap|.*msfconsole|.*\bncat|.*\bnmap|.*nikto|.*ettercap|.*tunnel\.(php|jsp|asp|py)|.*/nc\b|.*socks.(php|jsp|asp|py)|.*proxy.(php|jsp|asp|py)|.*brook.*|.*frps|.*frpc|.*aircrack|.*hydra|.*miner|.*fscan|.*/ew$' -type f | ag -v '/lib/python' | xargs -i{} ls -halt {}
    """
    return util.to_code(util.exec_cmd(command))

def get_file_transfer():
    command = 'cat /var/log/message* | ag "ZMODEM:.*BPS" --no-color'
    return util.to_code(util.exec_cmd(command))
