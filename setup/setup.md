Local Development Setup
=======================

These instructions assume you are using Mac OS X.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Install [Vagrant](http://downloads.vagrantup.com/)
3. Install Vagrant Guest Additions: `vagrant plugin install vagrant-vbguest`
4. Clone the Repository: `git clone https://github.com/heiskr/sagefy.git`
5. Enter the directory: `cd sagefy`
6. `vagrant up`
7. `sudo nano /etc/hosts`, and add `192.168.122.114 doris`
8. `cp server/config.dev.example.py server/config.py`
9. `vagrant ssh` into the Virtual Box.
10. Create dev data:
  ````
  cd /var/www/server
  python3 dev_data.py
  ````
11. Start up the web service:
  ````
  sudo uwsgi --stop /tmp/uwsgi-master.pid
  sudo uwsgi --ini /var/www/setup/uwsgi_local.ini
  ````
12. Start up the web client:
  ````
  pm2 start /var/www/client/app/index.server.js
  cd /var/www/client
  pm2 start npm -- start
  ````
13. Start up Nginx:
  ````
  sudo nginx -s stop
  sudo nginx -c /var/www/setup/nginx.conf
  ````
14. In your browser, visit `http://doris/s/`, there should be a welcome message.
15. In your browser, visit `http://doris/`, the home page should be working. Try to sign up for an account.

Note that pm2 is not properly watching JavaScript files. To rebuild the JS:

    pm2 restart all
    pm2 logs
    ++ then wait for it to say something like `Version: webpack 1.13.3`

_TODO: How much of this can be moved to the Vagrant provision script?_

Common Vagrant commands
-----------------------

- Enter Vagrant: `vagrant ssh`
- Put Vagrant to sleep: `vagrant suspend`
- Wake Vagrant back up: `vagrant up`
- Make a new Vagrant: `vagrant destroy; vagrant up`
- SSH locked? Try this: `vagrant halt -f; vagrant up; vagrant ssh`

Tailing the Logs
----------------

    sudo tail -F /var/log/nginx/error.log
    sudo tail -F /tmp/uwsgi.log
    pm2 logs

Deploy steps
------------

    ++ ssh into the server ++
    cd /var/www
    sudo git pull origin master
    cd client
    sudo npm run deploy
    sudo cp -a app/images/* distribution/ && sudo cp -a app/*.{html,txt,ico} distribution/
    pm2 restart all

Things to fix:

- The server should not know about git
- Fix permissions so we don't have to run `cp` by itself.
- We should need to restart uwsgi, which should not be in watch mode on prod.

Back up the database
--------------------

Set up:

    ++ ssh into the server ++
    sudo pip3 install --upgrade --ignore-installed b2
    cd /var/www
    mkdir dbbu

Run:

    ++ ssh into the server ++
    cd /var/www/dbbu
    today=`date '+%Y_%m_%d__%H_%M_%S'`
    sudo -u postgres pg_dump sagefy > "sagefy-$today.sql"
    b2 authorize_account xxx xxxxxxxx  # see dashlane
    b2 sync /var/www/dbbu b2:sagefy-dbbu

TODO:

- Set up as a cron job... find a smart person to fix the environment :)
