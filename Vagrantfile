# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure("2") do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.name = 'CEN4010-DEV'
    vb.memory = "1024"
  end

  # install python for ansible
  config.vm.provision "shell", inline: "sudo apt install python -y"

  config.vm.provision "playbook", type: "ansible_local" do |ansible|
    # ansible.verbose = "v"
    ansible.playbook="playbook.yml"

  end
  
end
