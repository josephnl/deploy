# /usr/bin/Python
# coding=utf-8
# diff_deploy.py

import configparser
import paramiko
import os
from datetime import date
# 因为使用了压缩,请安装7z作为压缩程序,并且把7z的路径添加到系统路径

def main():

    # 读取配置文件,注意configparser模块和函数的大小写

    cf = configparser.ConfigParser()
    cf.read("C:\\Work\\Joseph\\deploy\\config.ini")

    host = cf.get("server", "host")
    port = int(cf.get("server", "port"))
    user = cf.get("server", "user")
    passwd = cf.get("server", "passwd")
    project_path = cf.get("path", "project_path")
    server_base = cf.get("path", "server_base")
    deploy_base = cf.get("path", "deploy_base")

    # project_path = d:\workspace\east\src\main\webapp
    # deploy_path = d:\workspace\deploy


    # 准备打包列表
    pack_list = ['com', 'web', 'views', 'error', 'front', 'common']
    path_list = {
        'com':'\\WEB-INF\\classes',
        'web':'\\WEB-INF',
        'views':'\\WEB-INF',
        'front':'\\WEB-INF',
        'error':'\\WEB-INF',
        'common':''
        }

    # 准备全量发布的当天路径
    deploy_path = deploy_base + '\\' + str(date.today())
    os.system('mkdir '+ deploy_path)

    # 链接SFTP, 准备上传文件
    t = paramiko.Transport(host, port)
    t.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)

    # 打包全量发布需要的文件到发布文件目录 deploy path 并且上传服务器

    for pack in pack_list:
        # 打包文件
        des = deploy_path + '\\' + pack + '.zip'
        src = project_path + path_list[pack] + '\\' + pack + '\\*'
        zipcommand = '7z a -tzip -r "%s" "%s" ' % (des, src)
        os.system(zipcommand)
        print('file %s has been packed' % des)

        # 上传SERVER
        server_path = server_base + path_list[pack].replace('\\','/') + '/' + pack + '.zip'
        try:
            print('Uploading ****************************' + os.path.basename(des))
            sftp.put(des, server_path)
            print(' Uploading success\n')
        except FileNotFoundError:
            print(os.path.basename(des) + ' Uploading failed, server path not exist\n')

    # 关闭SFTP
    t.close()

if __name__ == '__main__':
    main()
