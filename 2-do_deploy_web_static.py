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
    if archive_path and not os.path.exists(archive_path):
        return False
    # Upload the archive_path to /tmp/ on the remote server
    put(archive_path, "/tmp/")
    # prepare the name of the archive on the server
    archive = archive_path[archive_path.find("/") + 1: -4]
    try:
        release_dir = "/data/web_static/releases/"
        # Prepare the archive folder inside /data/web_static/releases
        run(f"mkdir -p {release_dir}{archive}")
        # Unpack the tgz file to the releases
        run(f"tar -xzf /tmp/{archive}.tgz -C {release_dir}{archive}/")
        # Delete archive from /tmp
        run(f"rm /tmp/{archive}.tgz")
        #
        run(f"mv {release_dir}{archive}/web_static/* {release_dir}{archive}/")

        run(f"rm -rf {release_dir}{archive}/web_static")

        run("rm -rf /data/web_static/current")

        run("mkdir /data/web_static/current/")

        run(f"ln -sfn {release_dir}{archive}/* /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception:
        return False
