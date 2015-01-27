Vagrant.configure("2") do |config|
    config.vm.box = "trusty64uci"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    config.vm.provision "shell", path: "setup/provision_local.sh"
    config.vm.hostname = "doris"
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.network "forwarded_port", guest: 9200, host: 9200
    config.vm.network "forwarded_port", guest: 5601, host: 5601
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--cpus", "2", "--memory", "2048"]
    end
    config.vm.network "private_network", ip: "192.168.122.114"
end
