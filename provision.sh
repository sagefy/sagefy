#!/usr/bin/env bash

# Assumes ubuntu/xenial64
# Based on http://do.co/1FmILwq and http://do.co/1GkXg4m

# >>> Make sure to backup current Postgres data first!

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
sudo chown -R annina www
git clone TODO
# >>> TODO permissions? I hate sudo-ing all the time.

# >>> TODO install docker-compose

# >>> TODO Update server config.py

#### Install node to build index.js/index.css

sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo apt-get -y install python-software-properties python g++ make
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
cd /var/www/client
sudo npm install

# >>> TODO npm run deploy

# >>> TODO Restore production Postgres data

#### Setup DB backups

# >>> ssh into the server
sudo pip3 install --upgrade --ignore-installed b2
cd /var/www
mkdir dbbu

# Populate Elasticsearch
# >>> TODO fill in command

# >>> Verify, then update Cloudflare's DNS records!
