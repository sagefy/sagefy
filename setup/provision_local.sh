#!/usr/bin/env bash

#### Initialize ###############################################################

sudo apt-get -y update
# sudo apt-get -y upgrade
# sudo apt-get -y install language-pack-en
# sudo apt-get -y autoremove

#### Get Code #################################################################

sudo apt-get -y install git

#### Aliases ##################################################################

sudo rm -rf /var/www
sudo ln -fs /vagrant /var/www
cd /var/www

#### Python ###################################################################

sudo apt-get -y install python3-dev
sudo apt-get -y install python3-setuptools
sudo apt-get -y install python3-pip
sudo pip3 install -r /var/www/server/requirements.txt
sudo pip3 install pytest coverage flake8

#### Rethink ##################################################################

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get -y update
sudo apt-get -y install rethinkdb
# Restart with init.d
sudo chmod -R 777 /var/run
sudo cp /var/www/setup/rethinkdb.conf /etc/rethinkdb/instances.d/instance1.conf
sudo /etc/init.d/rethinkdb restart
# Securing RethinkDB: https://rethinkdb.com/docs/security/
# TODO-1 Use socks to access the admin UI

#### Elasticsearch ############################################################

sudo apt-get -y install openjdk-7-jre-headless
wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main" | sudo tee --append /etc/apt/sources.list
sudo apt-get -y update
sudo apt-get -y install elasticsearch
sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch start
cd /var/www
# Securing ElasticSearch: do.co/1JsVB2O
# TODO-0 network.bind_host
# TODO-0 script.disable_dynamic

#### Kibana ###################################################################

# TODO-2 Enable Kibana
# cd ~
# wget https://download.elasticsearch.org/kibana/kibana/kibana-4.0.0-beta3.tar.gz
# tar xvf kibana-4.0.0-beta3.tar.gz
# sudo mkdir -p /var/www/kibana
# sudo cp -R ~/kibana-4.0.0-beta3/* /var/www/kibana/
# rm kibana-4.0.0-beta3.tar.gz
# rm -R kibana-4.0.0-beta3
# cd /var/www/kibana
# ulimit -v unlimited
# TO RUN: ./bin/kibana
# cd /var/www

#### Redis ####################################################################

# Securing Redis: do.co/1nfZxt2
sudo apt-get -y install redis-server
# TODO-0 Renaming Dangerous Commands
# TODO-0 Setting Data Directory Ownership and File Permissions

#### Client Tooling ###########################################################

sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get -y install nodejs
sudo npm install -g gulp
cd /var/www/client
sudo npm install
gulp deploy

#### Server ###################################################################

cd /var/www
sudo apt-get -y install uwsgi
sudo apt-get -y install nginx
sleep 1
sudo uwsgi --stop /tmp/uwsgi-master.pid
sleep 1
sudo uwsgi --ini /var/www/setup/uwsgi_local.ini
sleep 1
sudo nginx -s stop
sleep 1
sudo nginx -c /var/www/setup/nginx.conf

# TODO-1 Setup file system monitoring do.co/1GfDGYN
# TODO-1 Setup Digital Ocean private networking do.co/1nrFJE3
# TODO-1 Setup loggly
# TODO-1 Setup automated backups (especially of RethinkDB)
# TODO-1 set up auto updating on ubuntu
# TODO-2 Re-read bit.ly/1mERm9F

echo "Hooray! Provisioned."
echo "For script and style watching, run gulp."
