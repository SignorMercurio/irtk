import os
import subprocess
import oss2

from util import install_tool, get_os_release
from config import config

upload_dir = config['file_transfer']['upload_dir']
download_dir = config['file_transfer']['download_dir']
oss = config['oss']
tools_dir = oss['tools_dir']

def init_oss_bucket():
    install_tool(get_os_release(), 'python-devel', 'python-devel', 'python-dev')
    auth = oss2.Auth(oss['ak'], oss['sk'])
    return oss2.Bucket(auth, oss['endpoint'], oss['bucket'])

def upload_to_oss(bucket, file_path=None):
    if file_path is None:
        file_path = input("[+] 本地文件路径：")
    dir_name, file_name = os.path.split(file_path)
    try:
        # if file_path represents a directory, then tar it
        if os.path.isdir(file_path):
            subprocess.run(f"cd {dir_name} && tar -zcf {file_name}.tar.gz {file_name}", shell=True)
            file_name += ".tar.gz"
        bucket.put_object_from_file(f"{upload_dir[1:]}/{file_name}", f"{dir_name}/{file_name}")
        print(f'[+] 文件 {file_name} 上传成功')
    except Exception as e:
        print(e)
        print(f'[!] 文件路径 {file_path} 不存在')

def download_from_oss(bucket, object_path=None):
    print("[+] 可下载文件：")
    list_oss_objects(bucket, f"{tools_dir}/")

    if object_path is None:
        object_path = input("[+] OSS Object 路径：")
    dir_name, file_name = os.path.split(object_path)
    try:
        # will not support downloading directory from OSS
        bucket.get_object_to_file(object_path, f"{download_dir}/{file_name}")
        print(f'[+] 文件 {file_name} 下载成功')
    except Exception as e:
        print(e)
        print(f'[!] 文件路径 {file_path} 不存在')

def list_oss_objects(bucket, prefix):
    for obj in oss2.ObjectIteratorV2(bucket, prefix=prefix):
        print("\t" + obj.key)
