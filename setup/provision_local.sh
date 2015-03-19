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

#### Python ###################################################################

sudo apt-get -y install python3-dev
sudo apt-get -y install python3-setuptools
sudo apt-get -y install python3-pip
sudo pip3 install -r /var/www/api/requirements.txt
sudo pip3 install pytest
sudo pip3 install coverage

#### Rethink ##################################################################

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get -y update
sudo apt-get -y install rethinkdb
rethinkdb --daemon --bind all

#### Elasticsearch ############################################################

sudo apt-get -y install openjdk-7-jre-headless
wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main" | sudo tee --append /etc/apt/sources.list
sudo apt-get -y update
sudo apt-get -y install elasticsearch
sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch start
# cd /usr/share/elasticsearch
# bin/plugin --install river-rethinkdb --url http://goo.gl/UkBm47
cd /var/www

#### Kibana ###################################################################

cd ~
wget https://download.elasticsearch.org/kibana/kibana/kibana-4.0.0-beta3.tar.gz
tar xvf kibana-4.0.0-beta3.tar.gz
sudo mkdir -p /var/www/kibana
sudo cp -R ~/kibana-4.0.0-beta3/* /var/www/kibana/
rm kibana-4.0.0-beta3.tar.gz
rm -R kibana-4.0.0-beta3
cd /var/www/kibana
ulimit -v unlimited
# TO RUN: ./bin/kibana
cd /var/www

#### Redis ####################################################################

sudo apt-get -y install redis-server

#### UI Tooling ###############################################################

sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get -y update
sudo apt-get -y install nodejs
sudo npm install -g gulp
cd /var/www/ui
sudo npm install
gulp deploy

#### Server ###################################################################

cd /var/www
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo uwsgi --stop /tmp/uwsgi-master.pid
sudo uwsgi --ini /var/www/setup/uwsgi_local.ini
sudo nginx -s stop
sudo nginx -c /var/www/setup/nginx.conf

echo "Hooray! Provisioned."
echo "For script and style watching, run gulp."
