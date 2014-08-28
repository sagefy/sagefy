#!/usr/bin/env bash

#### Initialize ###############################################################

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install language-pack-en
sudo apt-get -y autoremove

#### Get Code #################################################################

sudo apt-get -y install git

#### Aliases ##################################################################

sudo rm -rf /var/www
sudo ln -fs /vagrant /var/www

#### Rethink ##################################################################

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get -y update
sudo apt-get -y install rethinkdb
rethinkdb --daemon

#### Python ###################################################################

sudo apt-get -y install python2.7-dev
sudo apt-get -y install python-pip
sudo pip install -r /var/www/setup/requirements.txt
sudo pip install pytest
sudo pip install coverage

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
# TO LOG: sudo tail -F /tmp/uwsgi.log
# TO STOP: sudo uwsgi --stop /tmp/uwsgi-master.pid
sudo nginx -c /var/www/setup/nginx.conf
# TO STOP: sudo nginx -s stop    (/var/run/nginx.pid)

echo "Hooray! Provisioned."
echo "For script and style watching, run gulp."
