Local Development Setup
=======================

These instructions assume you are using Mac OS X.

Get Vagrant Running
-------------------

### 1. Install VirtualBox

    https://www.virtualbox.org/wiki/Downloads

### 2. Install Vagrant

    http://downloads.vagrantup.com/

### 3. Install Vagrant Guest Additions

    vagrant plugin install vagrant-vbguest

### 4. Clone the Repository

    mkdir ~/Sites  # Make a new Sites directory if needed
    cd ~/Sites  # Enter the Sites directory
    git clone https://github.com/heiskr/sagefy.git sagefy

### 5. Rev it up

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

How to Deploy
-------------

    ???

Tailing the Log
---------------

    sudo tail -F /tmp/uwsgi.log

Working with the UI
-------------------

    cd ~/Sites/sagefy/ui
    gulp

Push gh-pages to Github Pages
-----------------------------

    git subtree push --prefix gh-pages origin gh-pages
