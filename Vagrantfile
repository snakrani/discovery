# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

# Load Vagrant configurations (versioned and unversioned)
vm_config = YAML.load_file("vagrant-config.default.yml")
vm_config.merge!(YAML.load_file("vagrant-config.yml")) if File.exist?("vagrant-config.yml")

# Install extra Vagrant plugins
required_plugins = %w(vagrant-vbguest)

required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = vm_config["box_name"]
  config.vm.hostname = vm_config["server_name"]

  # If you want to listen at a specific local IP address
  # > add "ip_address: '###.###.###.###'" to your vagrant-config.yml
  if vm_config.has_key?("ip_address")
    config.vm.network "private_network", ip: vm_config["ip_address"]
  end

  config.vm.provider "virtualbox" do |v|
    v.name = vm_config["server_name"]
    v.memory = vm_config["memory_size"]
    v.cpus = vm_config["cpus"]
  end

  config.vm.provision :shell do |s|
    s.path = "scripts/bootstrap.sh"
    s.args   = [
      "/vagrant",
      vm_config["django_admin"],
      vm_config["django_admin_pw"],
      vm_config["django_admin_email"]
    ]
  end

  config.vm.network "forwarded_port", guest: 8000, host: vm_config["web_port"]
  config.vm.network "forwarded_port", guest: 5432, host: vm_config["db_port"]
  config.vm.network "forwarded_port", guest: 6379, host: vm_config["queue_port"]
end
