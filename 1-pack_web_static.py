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
