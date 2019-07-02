#!/usr/bin/env bash

# Assumes ubuntu/18.04
# Based on http://do.co/1FmILwq and http://do.co/1GkXg4m

# >>> Make sure to backup current Postgres data first!
# Run the backup process  (See docs/setup.md)
# Stop prod server
# download from B2 site

# Create a Droplet in Digital Ocean. Ubuntu 18.04/64, $5, SFO, all default options.
# !!! Add it to the Digital Ocean firewall !!!
# https://cloud.digitalocean.com/networking/firewalls

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

# Configure timezone
# http://unix.stackexchange.com/a/140739
sudo timedatectl set-timezone America/Los_Angeles

# Configure NTP
sudo apt-get -y update
sudo apt-get -y install ntp

# Create a swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo sh -c 'echo "/swapfile none swap sw 0 0" >> /etc/fstab'

# Install docker
sudo apt-get -y update
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo gpasswd -a ${USER} docker
sudo usermod -aG docker $USER
sudo service docker restart
docker --version

# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Get the code
sudo apt-get -y install git
sudo mkdir /var/sagefy
cd /var
sudo chown -R annina sagefy
sudo chmod -R 775 sagefy
git clone https://github.com/sagefy/sagefy.git sagefy
cd sagefy

# Update env
cd /var/sagefy/server
cp .env.example .env
nano .env
# >>> then update FIXME
# Also same for /postgres

#### Optional: Install node
# sudo apt-get -y update
# sudo apt-get -y install software-properties-common
# sudo apt-get -y install python-software-properties python g++ make
# curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
# sudo apt-get install -y nodejs

# Spin it all up
docker-compose up -d
# Takes 2-3 minutes

# >>> Restore production Postgres data
# From your computer...
scp ~/Desktop/sagefy-2018...sql annina@IPADDRESS:/var/sagefy/postgres
# Then on server, verify file with ls
cd /var/sagefy/postgres
ls
# Create the data
docker exec -it sagefy_postgres_1 psql -U sagefy -a -f /sagefy/sagefy-2018...sql
# verify with ` docker exec -it sagefy_postgres_1 psql -U sagefy `
# select count(*) from sg_public.user;

#### Setup DB backups
sudo apt-get install python-pip
sudo pip install --upgrade --ignore-installed b2
cd /var/sagefy
mkdir dbbu

# Set up Digital Ocean monitoring
curl -sSL https://agent.digitalocean.com/install.sh | sh

# >>> Verify it works using the IP Address
# Sign up for an account, log in to existing account, go through learning process.
# >>> Then update Cloudflare's DNS records!
# Finally, delete the old instance.
