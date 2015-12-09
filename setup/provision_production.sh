#!/usr/bin/env bash

#
# http://do.co/1FmILwq
#


##########
# Security Measures: http://do.co/1EyGQWz
#
# - [x] Use SSH Keys instead of passwords
# - [x] Enable Firewalls to restrict incoming port access
# - [ ] Use a virtual private network
# - [x] Use a public SSL certificate
# - [ ] Audit services
# - [ ] Use an intrusion detection system: OSSEC, Tripwire, Aide...
# - [ ] Run databases in isolated environments
#############

# Create a new user
adduser --disabled-password --gecos "" annina

# Add user to sudo group
gpasswd -a annina sudo

# TODO check for sagefy_rsa.pub, and if not, then exit and say `run ssh-keygen ...`

# Add SSH public key to user
su - annina
mkdir .ssh
chmod 700 .ssh
touch .ssh/authorized_keys
cat /var/www/setup/sagefy_rsa.pub >> .ssh/authorized_keys  # TODO file exists?
chmod 600 .ssh/authorized_keys
exit

# Disable root access
# http://stackoverflow.com/a/23370005
sed -i -r 's/^#?(PermitRootLogin) yes/\1 no/' /etc/ssh/sshd_config

# Restart SSH
service ssh restart

#
# http://do.co/1GkXg4m
#

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

# TODO Install stuff from provision local...
