Vagrant.configure("2") do |config|
  config.vm.box = "precise64uci"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.provision "shell", path: "provision_local.sh"
  config.vm.network :forwarded_port, host: 5656, guest: 80
  config.vm.network :forwarded_port, host: 8653, guest: 8653
end
