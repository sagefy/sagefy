Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision "shell", path: "provision_local.sh"
  config.vm.network :forwarded_port, host: 5656, guest: 80
  config.vm.network :forwarded_port, host: 8653, guest: 8653
end
