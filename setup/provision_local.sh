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

# Prod:
# sudo mkdir /var/www
# sudo chown -R annina www

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
sudo cp /var/www/setup/rethinkdb.conf /etc/rethinkdb/instances.d/instance1.conf
sudo /etc/init.d/rethinkdb restart
# Securing RethinkDB: https://rethinkdb.com/docs/security/
# TODO-1 Use socks to access the admin UI

#### Elasticsearch ############################################################

# Securing ElasticSearch: do.co/1JsVB2O
sudo apt-get -y install openjdk-7-jre-headless
wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.2.deb
sudo dpkg -i elasticsearch-1.7.2.deb
sudo update-rc.d elasticsearch defaults
echo "network.bind_host: localhost" | sudo tee -a /etc/elasticsearch/elasticsearch.yml
echo "script.disable_dynamic: true" | sudo tee -a /etc/elasticsearch/elasticsearch.yml
sudo service elasticsearch start

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
# Renaming Dangerous Commands
sudo tee -a /etc/redis/redis.conf <<- EOM
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG ""
rename-command SHUTDOWN ""
rename-command BGREWRITEAOF ""
rename-command BGSAVE ""
rename-command SAVE ""
rename-command DEBUG ""
EOM
# Setting Data Directory Ownership and File Permissions
sudo chmod 700 /var/lib/redis
sudo chown redis:root /etc/redis/redis.conf
sudo chmod 600 /etc/redis/redis.conf
sudo service redis-server restart

#### Client Tooling ###########################################################

sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
cd /var/www/client
sudo npm install
npm run deploy

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
echo "For script and style watching, run npm start."
echo "Be sure to update config.py if needed"
