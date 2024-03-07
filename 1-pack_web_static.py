#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo, using the function do_pack."""
import datetime
import os
from fabric.api import local


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    os.makedirs("versions", exist_ok=True)
    source_dir = "./web_static"
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")
    output_file = f"web_static_{timestamp}.tgz"
    if local(f"tar czf {output_file} {source_dir}").failed is True:
        return None
    if os.path.exists(output_file):
        return output_file
    else:
        return None
