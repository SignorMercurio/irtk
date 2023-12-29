import os
import subprocess
import time
from stat import S_ISDIR

import util
import ti

from util import local
from recon import recon
from config import config
from oss import init_oss_bucket, upload_to_oss, download_from_oss

upload_dir = config['file_transfer']['upload_dir']
download_dir = config['file_transfer']['download_dir']

def invoke_shell():
    if local:
        subprocess.run(['bash', '-li'])
        return
    channel = util.client.invoke_shell()
    channel.recv(1024)
    print(channel.recv(1024).decode(), end='')
    while True:
        cmd = input().strip()
        if cmd == "exit":
            break
        channel.send(cmd + "\n")
        while channel.recv_ready() is False:
            time.sleep(0.1)
        output = ""
        while channel.recv_ready():
            output += channel.recv(1024).decode()
        print(output.split('\n', 1)[1], end="")

def upload_to_remote():
    util.exec_cmd(f"mkdir -p {upload_dir}")
    sftp = util.client.open_sftp()
    file_path = input("[+] 本地文件路径：")
    dir_name, file_name = os.path.split(file_path)

    try:
        # if file_path represents a directory, then tar it
        if os.path.isdir(file_path):
            subprocess.run(f"cd {dir_name} && tar -zcf {file_name}.tar.gz {file_name}", shell=True)
            file_name += ".tar.gz"
        sftp.put(f"{dir_name}/{file_name}", f"{upload_dir}/{file_name}")
        print(f'[+] 文件 {file_name} 上传成功')
    except:
        print(f'[!] 文件路径 {file_path} 不存在')
    finally:
        sftp.close()

def download_from_remote():
    sftp = util.client.open_sftp()
    file_path = input("[+] 远程文件路径：")
    dir_name, file_name = os.path.split(file_path)

    try:
        # if file_path represents a directory, then tar it
        if S_ISDIR(sftp.stat(file_path).st_mode):
            util.exec_cmd(f"cd {dir_name} && tar -zcf {file_name}.tar.gz {file_name}")
            file_name += ".tar.gz"
        sftp.get(f"{dir_name}/{file_name}", f"{download_dir}/{file_name}")
        print(f'[+] 文件 {file_name} 下载成功')
    except:
        print(f'[!] 文件路径 {file_path} 不存在')
    finally:
        sftp.close()

def process_info():
    pid = input("[+] PID：")
    path = f"/proc/{pid}"
    print(util.exec_cmd(f"ps -ef | ag {pid} | ag -v 'ag|ps'"))
    print("cmdline: " + util.exec_cmd(f"cat {path}/cmdline"))
    print(util.exec_cmd(f"ls -l {path}/exe"))
    print(util.exec_cmd(f"ls -l {path}/cwd"))
    print("environ: " + util.exec_cmd(f"cat {path}/environ"))
    print(util.exec_cmd(f"cat {path}/status | head -n 10"))

if __name__ == "__main__":
    if not local:
        util.connect_to_host(config['ssh_info'])

    while True:
        print(f"\n=== irtk {'local' if local else 'remote'} ===")
        print("1. 信息收集")
        print("2. 生成终端以运行命令")
        if local:
            print(f"3. 上传文件到 OSS 的 {upload_dir[1:]}")
            print(f"4. 从 OSS 下载文件到 {download_dir}")
        else:
            print(f"3. 上传文件到 {upload_dir}")
            print(f"4. 下载文件到 {download_dir}")
        print("5. PID 快速查询进程")
        print("6. 威胁情报查询")
        print("7. 痕迹清除")
        print("8. 退出程序")

        choice = input("[+] 请输入：")
        if choice == "1":
            recon.go(local)
        elif choice == "2":
            invoke_shell()
        elif choice == "3":
            if local:
                bucket = init_oss_bucket()
                upload_to_oss(bucket)
            else:
                upload_to_remote()
        elif choice == "4":
            if local:
                bucket = init_oss_bucket()
                download_from_oss(bucket)
            else:
                download_from_remote()
        elif choice == "5":
            process_info()
        elif choice == "6":
            target = input("[+] 查询目标（远程文件路径/IP/哈希值）：")
            ti.search(target)
        elif choice == "7":
            util.exec_cmd(f"rm -rf {upload_dir}")
            print("[+] 痕迹清除完成")
        elif choice == "8":
            break
        else:
            print("[!] 非法输入")
