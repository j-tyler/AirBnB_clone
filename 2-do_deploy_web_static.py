#!/usr/bin/python3
"""Pack up web_static for shipping"""


from fabric.api import local
from datetime import datetime

env.hosts = ["54.145.142.123", "52.54.98.43"]


def do_pack():
    """Pack project for shipment"""
    fn = 'versions/web_static_{}.tgz'.format(
         datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    try:
        local("if [ ! -d versions ]; then\nmkdir versions\nfi")
        local("tar -cvzf {:s} web_static/".format(fn))
    except:
        return None
    return "{}".format(fn)


def do_deploy(archive_path):
    """Deploy packed project"""
    try:
        local("touch {:s}".format(archive_path))
    except:
        return False
    try:
        put(archive_path, "/tmp/{:s}".format(archive_path))
        sudo('tar xvzf {:s} -C /data/web_static/releases/{:s}'.format(
             archive_path, archive_path.split('.')[0]))
        sudo('rm -f /tmp/{:s}'.format(archive_path))
        sudo('rm -f /data/web_server/curent')
        sudo('ln -sf /data/web_static_releases/{:s} /data/web_server/current'.
             format(archive_path.split('.')[0]))
    except:
        return False
    return True
