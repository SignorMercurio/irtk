import util

def recon():
    output = "\n## 用户信息\n"

    output += f"#### 非默认用户\n{get_non_default_users()}\n"
    output += f"#### 特权用户\n{get_priv_users()}\n"
    output += f"#### 当前登录用户\n{get_logged_in_users()}\n"
    output += f"#### 可登录用户\n{get_users_can_login()}\n"
    output += f"#### 登录 IP\n{get_login_ip()}\n"
    output += f"#### 新增用户\n{get_new_users()}\n"
    output += f"#### sudoer 用户\n{get_sudoers()}\n"
    output += f"#### /etc/passwd 信息\n{util.get_file_stat('/etc/passwd')}\n"
    
    return output

def get_non_default_users():
    command = "grep '^UID_MIN' /etc/login.defs | awk '{print $2}'"
    min_uid = util.exec_cmd(command)
    command = "cat /etc/passwd | awk -F: '" + f'$3 >= {min_uid} && $3 != 65534 && $1 != "nobody"' +  " {print $0}'"
    return util.to_code(util.exec_cmd(command))

def get_priv_users():
    command = "cat /etc/passwd | ag -v '^root|^#|^(\+:\*)?:0:0:::' | awk -F: '{if($3==0) print $1}'"
    return util.to_code(util.exec_cmd(command))

def get_logged_in_users():
    command = "who"
    return util.to_code(util.exec_cmd(command))

def get_users_can_login():
    command = "cat /etc/passwd | ag -v 'nologin$|false$'"
    return util.to_code(util.exec_cmd(command))

def get_login_ip():
    command = "ag -a 'accepted' /var/log/secure* /var/log/auth.* 2>/dev/null | ag -o '\d+\.\d+\.\d+\.\d+' | sort | uniq"
    return util.to_code(util.exec_cmd(command))

def get_new_users():
    command = "ag -a 'new user' /var/log/secure* /var/log/auth.* 2>/dev/null | awk -F '[=,]' '{print $1,$2}' | awk '{print $1,$2,$3,$9}'"
    return util.to_code(util.exec_cmd(command))

def get_sudoers():
    command = "cat /etc/sudoers | ag -v '^#' | sed -e '/^$/d' | ag ALL= --nocolor"
    return util.to_code(util.exec_cmd(command))
