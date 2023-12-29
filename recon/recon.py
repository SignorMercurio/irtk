import datetime
import shutil

from config import config
from oss import init_oss_bucket, upload_to_oss

upload_dir = config['file_transfer']['upload_dir']
recon = config['recon']
mkdocs = config['mkdocs']

def go(local):
    from . import basic
    output, os_release, ip_addr, hostname = basic.recon()
    print('[+] 基础信息收集完成')

    if recon['users']:
        from . import users
        output += users.recon()
        print('[+] 用户信息收集完成')

    if recon['ssh']:
        from . import ssh
        output += ssh.recon()
        print('[+] SSH 信息收集完成')

    if recon['process']:
        from . import process
        output += process.recon()
        print('[+] 进程信息收集完成')

    if recon['network']:
        from . import network
        output += network.recon()
        print('[+] 网络信息收集完成')

    if recon['cron']:
        from . import cron
        output += cron.recon()
        print('[+] 计划任务信息收集完成')

    if recon['log']:
        from . import log
        output += log.recon()
        print('[+] Web 日志信息收集完成')

    if recon['files']:
        from . import files
        output += files.recon()
        print('[+] 文件信息收集完成')

    if recon['env']:
        from . import env
        output += env.recon()
        print('[+] 环境变量信息收集完成')

    if recon['service']:
        from . import service
        output += service.recon()
        print('[+] 服务信息收集完成')

    if recon['rootkit']:
        from . import rootkit
        output += rootkit.recon()
        print('[+] Rootkit 检测完成')

    title = f'{os_release}_{ip_addr}_{hostname}_{datetime.date.today()}'
    output_path = f'./output/{title}.md'
    # write to file
    with open(output_path, 'w') as outfile:
        outfile.write(output)
    print(f'[+] 输出结果至文档完成：{output_path}')

    url = ''
    if local:
        bucket = init_oss_bucket()
        upload_to_oss(bucket, output_path)
        url = f'oss://{bucket.bucket_name}/{upload_dir[1:]}/{title}.md'
        print('[+] 已上传至 OSS：' + url)
    # in remote mode, we can write to mkdocs
    elif mkdocs['enabled']:
        shutil.copyfile(output_path, f'{mkdocs["path"]}/{title}.md')
        url = f'{mkdocs["endpoint"]}/{title}'
        print('[+] 输出结果至 MkDocs 完成：' + url)
    
    return url
