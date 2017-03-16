#!/usr/bin/python3
"""Pack up web_static for shipping"""


from fabric.api import local
from datetime import datetime


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
