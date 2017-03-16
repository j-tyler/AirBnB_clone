#!/usr/bin/python3
"""Pack up web_static for shipping"""


from fabric.api import *
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
        fn = archive_path.split('/')[-1]
        version = fn.split('.')[0]
        path = '/data/web_static/releases'
        put(archive_path, "/tmp/{:s}".format(fn))
        sudo("mkdir -p /data/web_static/releases/{:s}".format(version))
        sudo('tar xvzf /tmp/{:s} -C /data/web_static/releases/{:s}'.format(
             fn, version))
        sudo('mv {:s}/{:s}/web_static/* {:s}/{:s}'.format(
            path, version, path, version))
        sudo('rm -f /tmp/{:s}'.format(fn))
        sudo('rm -f /data/web_static/current')
        sudo('ln -sf /data/web_static/releases/{:s} /data/web_static/current'.
             format(version))
    except:
        return False
    return True
