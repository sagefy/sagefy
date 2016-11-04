Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/xenial64"
    config.vm.network "private_network", ip: "192.168.122.114"
    config.vm.hostname = "doris"
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--cpus", "2", "--memory", "2048"]
    end
    config.vm.provision "shell", path: "setup/provision_local.sh"
end
