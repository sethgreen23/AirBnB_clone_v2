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
    """ distributes the archive to the server """
    if not os.path.exists(archive_path):
        return False

    try:
        # Put the archive on the server
        put(archive_path, '/tmp')

        # Extract archive filename without extension
        raw_name = os.path.basename(archive_path)[:-4]

        # Define remote paths
        releases_path = '/data/web_static/releases'
        current_path = '/data/web_static/current'

        # Create directory structure
        run(f"mkdir -p {releases_path}/{raw_name}/")

        # Extract archive contents
        run(f"tar -xzf /tmp/{raw_name}.tgz -C {releases_path}/{raw_name}/")

        # Remove archive file
        run(f"rm /tmp/{raw_name}.tgz")

        # Move contents to appropriate location
        run("mv {}/{}/web_static/* {}/{}/".format(releases_path, raw_name,
                                                  releases_path, raw_name))

        # Remove empty web_static directory
        run(f"rm -rf {releases_path}/{raw_name}/web_static")

        # Update symbolic link
        run(f"rm -rf {current_path}")
        run(f"ln -s {releases_path}/{raw_name}/ {current_path}")

        print("New version deployed!")
        return True

    except Exception as e:
        return False
