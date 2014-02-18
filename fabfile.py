from fabric.api import run


def restart_uwsgi():
    """
    Reloads master uwsgi process.
    """
    run("sudo uwsgi --reload /tmp/uwsgi-master.pid")


def restart_nginx():
    """
    Restarts master nginx process.
    """
    run("sudo /usr/sbin/nginx -s reload")
