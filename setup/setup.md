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
8. In your browser, visit `http://doris/`

Crap I Shouldn't Need to Do
----------------------------

... after creating a new box

    sudo uwsgi --stop /tmp/uwsgi-master.pid
    sudo uwsgi --ini /var/www/setup/uwsgi_local.ini
    sudo nginx -s stop
    sudo nginx -c /var/www/setup/nginx.conf
    pm2 start /var/www/client/app/index.server.js
    cd /var/www/server
    python3 dev_data.py
    cd /var/www/client
    pm2 start npm -- start
    pm2 logs


Common Vagrant commands
-----------------------

- Enter Vagrant: `vagrant ssh`
- Put Vagrant to sleep: `vagrant suspend`
- Make a new Vagrant: `vagrant destroy; vagrant up`

Tailing the Log
---------------

    sudo tail -F /var/log/nginx/error.log
    sudo tail -F /tmp/uwsgi.log

Working with the UI
-------------------

    cd ~/Sites/sagefy/ui
    npm start

Push gh-pages to Github Pages
-----------------------------

    git subtree push --prefix gh-pages origin gh-pages


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
    mkdir rethinkdb-bu

Run:

    ++ ssh into the server ++
    cd /var/www/rethinkdb-bu
    rethinkdb dump
    b2 authorize_account xxx xxxxxxxx  # see dashlane
    b2 sync /var/www/rethinkdb-bu b2:sagefy-rethinkdb-backup2

TODO:

- Set up as a cron job... find a smart person to fix the environment :)
