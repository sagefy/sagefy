from fabric.api import run, cd


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


def deploy_gulp():
    """
    Update JS and CSS.
    """
    with cd("/var/www/ui"):
        run("sudo npm install")
        run("bower install -F --allow-root")
        run("gulp deploy")
