#!/usr/bin/env bash

# Assumes ubuntu/xenial64
# Based on http://do.co/1FmILwq and http://do.co/1GkXg4m

# >>> Make sure to backup current Postgres data first!
# Run the backup process  (See SETUP.md)
# Stop prod server
# download from B2 site

# Create a Droplet in Digital Ocean. Ubuntu 16/64, $5, SFO, all default options.
# Then log in with `ssh root@IPADDRESS`. Look in your email for the root password.
# It will make you change the root password on log in. Write this down temporarily.

# Create a new user
adduser --gecos "" annina

# Add user to sudo group
gpasswd -a annina sudo

# Add SSH public key to user
su - annina
mkdir .ssh
chmod 700 .ssh
touch .ssh/authorized_keys
nano .ssh/authorized_keys
# >>> Copy sagefy_rsa.pub into authorized_keys
chmod 600 .ssh/authorized_keys
exit

# Disable root access http://stackoverflow.com/a/23370005
sed -i -r 's/^#?(PermitRootLogin) yes/\1 no/' /etc/ssh/sshd_config

# Restart SSH
service ssh restart

# Use new user
su - annina

# Configure firewall
sudo ufw allow 22  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 25/tcp  # SMTP
sudo ufw enable

# Configure timezone
# http://unix.stackexchange.com/a/140739
sudo timedatectl set-timezone America/Los_Angeles

# Configure NTP
sudo apt-get update
sudo apt-get install ntp

# Create a swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo sh -c 'echo "/swapfile none swap sw 0 0" >> /etc/fstab'

# Get the latest set of packages
sudo apt-get -y update

# Get the code
sudo apt-get -y install git
sudo mkdir /var/www
cd /var
sudo chown -R annina www
sudo chmod -R 775 www
git clone https://github.com/heiskr/sagefy.git www
cd www

# Install docker-compose
sudo apt-get update
sudo apt-get install \
  apt-transport-https \
  ca-certificates \
  curl \
  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce=17.09.0~ce-0~ubuntu
sudo gpasswd -a ${USER} docker
sudo usermod -aG docker $USER
sudo service docker restart
docker --version

sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# Takes about 2 minutes...
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# from https://svenv.nl/unixandlinux/dockerufw/
sudo nano /etc/default/ufw
# change DEFAULT_FORWARD_POLICY="ACCEPT"
sudo ufw allow 2375/tcp
sudo ufw reload
sudo nano /etc/default/docker
# enable and add: DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 --iptables=false"
sudo service docker restart
sudo nano /etc/ufw/before.rules
# Add these lines JUST BEFORE “*filter”.
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING ! -o docker0 -s 172.17.0.0/16 -j MASQUERADE
COMMIT
sudo reboot now
sudo touch /etc/docker/daemon.json
sudo nano /etc/docker/daemon.json
# contents: {"iptables": false}
sudo service docker stop
sudo service docker start

# Now `logout` and ssh back into the server.

# Update server config.py
cd /var/www
cp server/config_prod.py server/config.py
nano server/config.py
# >>> then update mail_sender and mail_password

#### Install node to build index.js/index.css
sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
yarn global add pm2
cd /var/www/client
yarn install
yarn run deploy

# Spin it all up
docker-compose up -d
# Takes 2-3 minutes

# >>> Restore production Postgres data
# From your computer...
scp ~/Desktop/sagefy-2018...sql annina@IPADDRESS:/var/www/postgres
# Then on server, verify file with ls
cd /var/www/postgres
ls
# Create the data
docker exec -it www_postgres_1 psql -U sagefy -a -f /www/sagefy-2018...sql
# verify with ` docker exec -it www_postgres_1 psql -U sagefy `
# select count(*) from users;
# select count(*) from subjects;
# select count(*) from units;
# select count(*) from cards;

#### Setup DB backups
sudo apt-get install python-pip
sudo pip install --upgrade --ignore-installed b2
cd /var/www
mkdir dbbu

# Populate Elasticsearch
cd /var/www
docker-compose run server python es_populate.py

# >>> Verify it works using the IP Address
# Sign up for an account, log in to existing account, go through learning process.
# >>> Then update Cloudflare's DNS records!
# Finally, delete the old instance.

##########
# Security Measures: http://do.co/1EyGQWz
#
# - [x] Use SSH Keys instead of passwords
# - [x] Enable Firewalls to restrict incoming port access
# - [ ] Use a virtual private network do.co/1nrFJE3
# - [x] Use a public SSL certificate
# - [ ] Audit services
# - [ ] Use an intrusion detection system: OSSEC, Tripwire, Aide... do.co/1GfDGYN
# - [x] Run databases in isolated environments
# - [ ] Setup loggly
# - [ ] Setup automated backups (especially of PostgresQL)
# - [ ] Setup auto updating on ubuntu
# - [ ] Re-read bit.ly/1mERm9F
#############
