#!/usr/bin/env bash

#### Initialize ###############################################################

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install language-pack-en

#### Get Code #################################################################

sudo apt-get -y install git

#### Aliases ##################################################################

sudo rm -rf /var/www
sudo ln -fs /vagrant /var/www

#### PostgreSQL ###############################################################

sudo apt-get -y install python-dev
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

#### Python ###################################################################

sudo apt-get -y install python-pip
sudo pip install -r /var/www/setup/requirements.txt
sudo pip install pytest

#### Migrations ###############################################################

cd /var/www/api
sudo -u postgres psql --username=postgres <<EOF
CREATE USER sagefy password 'sagefy' SUPERUSER;
CREATE DATABASE sagefy;
EOF
alembic upgrade head

#### Redis ####################################################################

sudo apt-get -y install redis-server

#### UI Tooling ###############################################################

sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get -y update
sudo apt-get -y install nodejs
sudo npm install -g gulp bower
cd /var/www/ui
sudo npm install
bower install -F --allow-root
gulp deploy

#### Server ###################################################################

cd /var/www
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo uwsgi --ini /var/www/setup/uwsgi_local.ini
# TO STOP: sudo uwsgi --stop /tmp/uwsgi-master.pid
sudo nginx -c /var/www/setup/nginx.conf
# TO STOP: sudo nginx -s stop    (/var/run/nginx.pid)

echo "Hooray! Provisioned."
echo "For script and style watching, run gulp."
