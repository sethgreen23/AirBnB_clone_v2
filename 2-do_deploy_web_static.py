#!/usr/bin/python3
""" Module to pack the files in tar file """
from fabric.api import local, task, run, put, sudo
from datetime import datetime
from fabric.context_managers import env
import os


env.hosts = ['34.229.161.215', '54.146.90.232']


@task
def do_pack():
    """ pack the folders inside an archive"""
    try:
        d = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        print("Packing web_static to versions/web_static_{}.tgz".format(d))
        if not os.path.exists("versions"):
            os.makedirs("versions")
        com = "tar -cvzf versions/web_static_{}.tgz web_static".format(d)
        result = local(com, capture=False)
        if not result.failed:
            size = os.path.getsize("versions/web_static_{}.tgz".format(d))
            form = "web_static packed: versions/web_static_{}.tgz -> {}Bytes"
            print(form.format(d, size))
            return "versions/web_static_{}.tgz".format(d)
        else:
            return None
    except Exception as e:
        return None


@task
def do_deploy(archive_path):
    """ deploy of static files on servers """
    if not os.path.exists(archive_path):
        return False
    try:
        f = archive_path.split("/")[-1]
        file_n = f.split(".")[0]
        dest_path = "/tmp"
        put(archive_path, dest_path)
        run("mkdir -p /data/web_static/releases/{}/".format(file_n))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(f,
                                                                       file_n))
        run("rm /tmp/{}".format(f))
        source = "/data/web_static/releases/{}/web_static/*".format(file_n)
        dest = "/data/web_static/releases/{}/".format(file_n)
        run("mv {} {}".format(source, dest))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file_n))
        run("rm -rf /data/web_static/current")
        alias = "/data/web_static/current"
        s_alias = "/data/web_static/releases/{}/".format(file_n)
        run("ln -s {} {}".format(s_alias, alias))
        print("New version deployed!")
        return True
    except Exception as e:
        return False
