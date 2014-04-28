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

# Schema Migration TODO: move to Alembic
FILES=/var/www/api/migrations/*.sql
for f in $FILES
do
    sudo -u postgres psql --username=postgres -f $f
done

#### Python ###################################################################

sudo apt-get -y install python-pip
sudo pip install -r /var/www/setup/requirements_local.txt

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
sudo cp /var/www/setup/uwsgi_upstart_local.conf /etc/init/uwsgi.conf
sudo cp /var/www/setup/nginx_upstart.conf /etc/init/nginx.conf
sudo initctl start uwsgi
sudo initctl start nginx

echo "Hooray! Provisioned."
echo "For script and style watching, run gulp."
