Local Development Setup
=======================

These instructions assume you are using Mac OS X.

Get Vagrant Running
-------------------

### Install VirtualBox

    https://www.virtualbox.org/wiki/Downloads

### Install Vagrant

    http://downloads.vagrantup.com/

### In your Terminal

    mkdir ~/Sites  # Make a new Sites directory if needed
    cd ~/Sites  # Enter the Sites directory
    git clone https://github.com/heiskr/sagefy.git sagefy
    cd sagefy  # Go into directory
    vagrant up  # Startup the virtual machine

View Local Development
----------------------

- `sudo nano /etc/hosts`, and add `192.168.122.114  doris`
- In your browser, visit `http://doris/`

Shut down Vagrant
-----------------

    control-c  # This stops the current task
    control-d  # Exits Vagrant's ssh
    vagrant suspend  # Store an image of Vagrant into memory

Start up Vagrant again
----------------------

    cd ~/Sites/sagefy
    vagrant up

Update Vagrant
--------------

    # This assumes you are not in Vagrant's ssh
    cd ~/Sites/sagefy
    vagrant provision

Make a new Vagrant
------------------

    # This assumes you are not in Vagrant's ssh
    cd ~/Sites/sagefy
    vagrant destroy
    vagrant up
