# /usr/bin/Python
# coding=utf-8
# diff_deploy.py

import configparser
import paramiko
import os

def main():
    # 读取配置文件,注意configparser模块和函数的大小写

    cf = configparser.ConfigParser()
    cf.read("C:\\Work\\Joseph\\deploy\\config.ini")

    host = cf.get("server", "host")
    port = int(cf.get("server", "port"))
    user = cf.get("server", "user")
    passwd = cf.get("server", "passwd")
    local_path = cf.get("path", "local_path")
    project_path = cf.get("path", "project_path")
    server_path = cf.get("path", "server_path")


    # 拼接本地目录
    webinf_path = local_path + '\\webapp\\WEB-INF'
    java_path = local_path + '\\java'
    webapp_path = local_path + '\\webapp'

    # 从SVN 导出拆分的包到本地local_path, 有jsp和JAVA文件
    # 准备拆分发布文件列表, 把所有JAVA文件对应的CLASS找到,并且复制到WEB-INF下
    # 因为windows不支持os.path.walk 利用dir命令,查找java_path目录下的所有java文件

    listdir_cmd = 'dir ' + java_path + ' /aa /s /b'
    file_list = os.popen(listdir_cmd).readlines()

    for java_file in file_list:
        classfile_src = project_path + '\\WEB-INF\\classes'+ java_file[len(java_path):-5] + 'class'
        classfile_des = webinf_path + '\\classes' + java_file[len(java_path):-5] + 'class'
        os.system('mkdir ' + os.path.dirname(classfile_des)) # 建目录
        os.system('copy ' + classfile_src + ' ' + classfile_des) # copy文件
        print(os.path.basename(classfile_des) + ' has being copyed\n')

    # 链接SFTP, 上传文件
    t = paramiko.Transport(host, port)
    t.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)

    # 准备需要拆分上传的文件列表,基于webapp, 因为所有CLASS文件已经在WEB-INF下面
    # 这里还没有做远程路径不存在的情况,后续增加

    listdir_cmd = 'dir ' + webinf_path + ' /aa /s /b'
    file_list = os.popen(listdir_cmd).readlines()
    print(file_list)

    for file in file_list:
        src = file[0:-1]
        des = server_path + file[len(webapp_path):-1].replace('\\','/')
        try:
            sftp.put(src, des)
            print(os.path.basename(des) + ' Uploading success\n')
        except FileNotFoundError:
            print(os.path.basename(des) + ' Uploading failed, server path not exist\n')

    t.close()

if __name__ == '__main__':
    main()
