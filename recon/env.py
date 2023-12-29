import util

def recon():
    output = "\n## 环境变量信息\n"

    output += f"#### env\n{get_env()}\n"
    output += f"#### /root/.bashrc\n{get_bashrc()}\n"
    output += f"#### /root/.bash_profile\n{get_bash_profile()}\n"
    output += f"#### /etc/profile\n{get_etc_profile()}\n"
    output += f"#### /etc/profile.d\n{get_etc_profiled()}\n"
    output += f"#### /etc/environment\n{get_etc_environment()}\n"
    output += f"#### LD_PRELOAD 等变量\n{get_ld_preload()}\n"
    output += f"#### /etc/ld.so.preload\n{get_ld_so_preload()}\n"
    output += f"#### 别名\n{get_alias()}\n"

    return output

def get_env():
    command = "env"
    return util.to_code(util.exec_cmd(command))

def get_bashrc():
    command = "cat /root/.bashrc"
    return util.to_code(util.exec_cmd(command))

def get_bash_profile():
    command = "cat /root/.bash_profile"
    return util.to_code(util.exec_cmd(command))

def get_etc_profile():
    command = "cat /etc/profile"
    return util.to_code(util.exec_cmd(command))

def get_etc_profiled():
    command = "ls -halt /etc/profile.d"
    return util.to_code(util.exec_cmd(command))

def get_etc_environment():
    command = "cat /etc/environment"
    return util.to_code(util.exec_cmd(command))

def get_ld_preload():
    command = """
    echo -e "LD_PRELOAD=$LD_PRELOAD\nLD_ELF_PRELOAD=$LD_ELF_PRELOAD\nLD_AOUT_PRELOAD=$LD_AOUT_PRELOAD\nPROMPT_COMMAND=$PROMPT_COMMAND\nLD_LIBRARY_PATH=$LD_LIBRARY_PATH"
    """
    return util.to_code(util.exec_cmd(command))

def get_ld_so_preload():
    command = "cat /etc/ld.so.preload"
    return util.to_code(util.exec_cmd(command))

def get_alias():
    command = "alias | ag -v 'git'"
    return util.to_code(util.exec_cmd(command))
