#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy"""
import datetime
import os
from fabric.api import local, run, put, env, sudo

env.hosts = ['ubuntu@34.207.237.37', 'ubuntu@35.175.65.10']


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    if os.path.isdir("versions") is False:
        local("mkdir -p versions")
    source_dir = "./web_static"
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")
    output_file = f"versions/web_static_{timestamp}.tgz"
    if local(f"tar czf {output_file} {source_dir}").failed is True:
        return None
    if os.path.exists(output_file):
        return output_file
    else:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers, using the
function do_deploy"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as ex:
        return False
