""" Module to pack the files in tar file """
from fabric.api import local, task
from datetime import datetime
import os


@task
def do_pack():
    """ pack the folders """
    d = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static".format(d),
                   capture=False)
    if not result.failed:
        for _, _, files in os.walk("versions"):
            for file_name in files:
                rel_file = os.path.join("versions", file_name)
                return rel_file
    else:
        return None
