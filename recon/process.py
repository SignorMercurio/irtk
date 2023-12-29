import util

from config import config

process = config['process']
cpu_top = process['cpu_top']
mem_top = process['mem_top']

def recon():
    output = "\n## 进程信息\n"

    output += f"#### CPU 占用前 {cpu_top} 进程\n{get_cpu_top_process()}\n"
    output += f"#### 内存占用前 {mem_top} 进程\n{get_mem_top_process()}\n"
    output += f"#### bash 反弹 shell 检查\n{bash_rev_shell_check()}\n"
    output += f"#### 挖矿进程检查\n{miner_check()}\n"
    output += f"#### 进程列表\n{get_aux()}\n"

    return output

def get_cpu_top_process():
    command = """
    echo "USER\tPID\t%CPU\t%MEM\tSTART\tTIME\tCOMMAND" | cat - <(ps aux | awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$9"\t"$10"\t"$11}' | grep -v ^'USER' | sort -rn -k3 | head -""" + str(cpu_top) + ") | column -t"

    return util.to_code(util.exec_cmd(command))

def get_mem_top_process():
    command = """
    echo "USER\tPID\t%CPU\t%MEM\tSTART\tTIME\tCOMMAND" | cat - <(ps aux | awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$9"\t"$10"\t"$11}' | grep -v ^'USER' | sort -rn -k4 | head -""" + str(mem_top) + ") | column -t"

    return util.to_code(util.exec_cmd(command))

def bash_rev_shell_check():
    command = "ps -ef | ag 'bash -i' | ag -v 'ag' | awk '{print $2}' | xargs -i{} lsof -p {} | ag 'ESTAB' --nocolor"
    return util.to_code(util.exec_cmd(command))

def miner_check():
    command = """
    ps aux | ag "systemctI|kworkerds|init10.cfg|wl.conf|crond64|watchbog|sustse|donate|proxkekman|test.conf|/var/tmp/apple|/var/tmp/big|/var/tmp/small|/var/tmp/cat|/var/tmp/dog|/var/tmp/mysql|/var/tmp/sishen|ubyx|cpu.c|tes.conf|psping|/var/tmp/java-c|pscf|cryptonight|sustes|xmrig|xmr-stak|suppoie|ririg|/var/tmp/ntpd|/var/tmp/ntp|/var/tmp/qq|/tmp/qq|/var/tmp/aa|gg1.conf|hh1.conf|apaqi|dajiba|/var/tmp/look|/var/tmp/nginx|dd1.conf|kkk1.conf|ttt1.conf|ooo1.conf|ppp1.conf|lll1.conf|yyy1.conf|1111.conf|2221.conf|dk1.conf|kd1.conf|mao1.conf|YB1.conf|2Ri1.conf|3Gu1.conf|crant|nicehash|linuxs|linuxl|Linux|crawler.weibo|stratum|gpg-daemon|jobs.flu.cc|cranberry|start.sh|watch.sh|krun.sh|killTop.sh|cpuminer|/60009|ssh_deny.sh|clean.sh|\./over|mrx1|redisscan|ebscan|barad_agent|\.sr0|clay|udevs|\.sshd|/tmp/init|xmr|xig|ddgs|minerd|hashvault|geqn|\.kthreadd|httpdz|pastebin.com|sobot.com|kerbero|2t3ik|ddgs|qW3xt|ztctb" | ag -v 'ag'
    """
    return util.to_code(util.exec_cmd(command))

def get_aux():
    command = "ps aux | ag -v 'systemd|auditd|polkitd|dbus-daemon|chronyd|gssproxy|rpcbind|dhclient|qmgr|rsyslogd|crond|atd|agetty|pickup|ps|awk|aegis|argusagent|assist_daemon|aliyun|tuned'"
    return util.to_code(util.exec_cmd(command))
