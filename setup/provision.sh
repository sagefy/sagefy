#!/usr/bin/env bash

#### Initialize ###############################################################

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install language-pack-en

#### Get Code #################################################################

sudo apt-get -y install git
git clone https://github.com/heiskr/sagefy.git /sagefy
cd /sagefy
git remote add upstream https://github.com/heiskr/sagefy.git

#### Aliases ##################################################################

sudo rm -rf /var/www
sudo ln -fs /sagefy /var/www

#### PostgreSQL ###############################################################

sudo apt-get -y install python-dev
sudo apt-get -y install postgresql-9.1
sudo apt-get -y install libpq-dev

#### Python ###################################################################

sudo apt-get -y install python-pip
sudo pip install -r /var/www/setup/requirements.txt

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

#### Server ###################################################################

cd /var/www
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo cp /var/www/setup/uwsgi_upstart.conf /etc/init/uwsgi.conf
sudo cp /var/www/setup/nginx_upstart.conf /etc/init/nginx.conf
sudo initctl start uwsgi
sudo initctl start nginx

echo "Now you should run the deploy script"
