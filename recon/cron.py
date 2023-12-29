import util

def recon():
    output = "\n## 计划任务信息\n"

    output += f"#### crontab\n{get_crontab()}\n"
    output += f"#### 计划任务列表\n{get_cronjobs()}\n"
    output += f"#### 可疑计划任务\n{get_susp_cron()}\n"

    return output

def get_crontab():
    command = "crontab -l"
    return util.to_code(util.exec_cmd(command))

def get_cronjobs():
    command = "ls -halt /etc/cron.*/*"
    return util.to_code(util.exec_cmd(command))

def get_susp_cron():
    command = "ag '((?:useradd|groupadd|chattr)|(?:wget\s|curl\s|tftp\s\-i|scp\s|sftp\s)|(?:bash\s\-i|fsockopen|nc\s\-e|sh\s\-i|\"/bin/sh\"|\"/bin/bash\"))' /etc/cron* /var/spool/cron/* --nocolor"
    return util.to_code(util.exec_cmd(command))
