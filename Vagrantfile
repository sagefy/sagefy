Vagrant.configure("2") do |config|
    config.vm.box = "precise64uci"
    config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
    config.vm.provision "shell", path: "setup/provision_local.sh"
    config.vm.hostname = "doris"
    config.vm.network "private_network", ip: "192.168.122.114"
end
