#!/usr/bin/env bash

#### Initialize ###############################################################

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install language-pack-en

#### Aliases ##################################################################

#### PostgreSQL ###############################################################

sudo apt-get -y install python-dev
sudo apt-get -y install postgresql-9.1
sudo apt-get -y install libpq-dev

#### Python ###################################################################

sudo apt-get -y install python-pip
sudo pip install -r /vagrant/api/requirements.txt

#### Redis ####################################################################

sudo apt-get -y install redis-server

#### Stylus and CoffeeScript ##################################################

sudo apt-get -y install npm
sudo npm install -g coffee-script stylus
sudo ln -s /usr/bin/nodejs /usr/bin/node
echo 'export NODE_PATH=/usr/local/lib/node_modules' >> ~/.bashrc

#### Server ###################################################################

cd /var/www
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo uwsgi  --http :8652 \
            --pythonpath /vagrant/api \
            --wsgi index:app \
            --processes 4 \
            --threads 2 \
            --daemonize /tmp/uwsgi.log
sudo nginx -c /vagrant/nginx.conf

echo "Hooray! Provisioned."
