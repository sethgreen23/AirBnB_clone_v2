#!/usr/bin/python3
""" Module to pack the files in tar file """
from fabric.api import local, task
from datetime import datetime
import os


@task
def do_pack():
    """ pack the folders """
    d = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    print("Packing web_static to versions/web_static_{}.tgz".format(d))
    if not os.path.exists("versions"):
        os.makedirs("versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static".format(d),
                   capture=False)
    if not result.failed:
        size = os.path.getsize("versions/web_static_{}.tgz".format(d))
        form = "web_static packed: versions/web_static_{}.tgz -> {}Bytes"
        print(form.format(d, size))
        return "versions/web_static_{}.tgz".format(d)
    else:
        return None
