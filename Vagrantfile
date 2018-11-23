# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Load Vagrant configurations (versioned and unversioned)
vm_config = YAML.load_file("vagrant/config.default.yml")
vm_config.merge!(YAML.load_file("vagrant/config.yml")) if File.exist?("vagrant/config.yml")

Vagrant.configure("2") do |config|
  vagrant_home = "/home/vagrant"
  project_directory = "/vagrant"

  config.vm.box = vm_config["box_name"]
  config.vm.hostname = vm_config["server_name"]

  if vm_config.has_key?("ip_address")
    config.vm.network :private_network, ip: vm_config["ip_address"]
  end

  config.vm.provider :virtualbox do |v|
    v.name = vm_config["server_name"]
    v.memory = vm_config["memory_size"]
    v.cpus = vm_config["cpus"]
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end

  if vm_config["copy_ssh"]
    # DO NOT overwrite the authorized_keys file on Vagrant
    if File.exist?("~/.ssh/config")
      config.vm.provision :file, source: "~/.ssh/config", destination: ".ssh/config"
    end

    Dir.glob("#{Dir.home}/.ssh/id_*") do |key_file|
      key_file = key_file.sub("#{Dir.home}/", '')
      config.vm.provision :file, source: "~/#{key_file}", destination: key_file
    end
  end
  if vm_config["copy_gitconfig"]
    config.vm.provision :file, source: "~/.gitconfig", destination: ".gitconfig"
  end

  if vm_config["copy_vimrc"]
    config.vm.provision :file, source: "~/.vimrc", destination: ".vimrc"
  end

  if vm_config["copy_profile"]
    config.vm.provision :file, source: "~/.profile", destination: ".profile"
  end
  if vm_config["copy_bash_aliases"]
    config.vm.provision :file, source: "~/.bash_aliases", destination: ".bash_aliases"
  end
  if vm_config["copy_bashrc"]
    config.vm.provision :file, source: "~/.bashrc", destination: ".bashrc"
  end
  config.vm.provision :shell do |s|
    s.name = "Bash startup additions (scripts/vagrant-bash)"
    s.inline = <<-SHELL
      if ! grep -q -F '#<<discovery>>' "${HOME}/.bashrc" 2>/dev/null
      then
        cat "${PROJECT_DIR}/scripts/vagrant-bash.sh" >> "${HOME}/.bashrc"
      fi
    SHELL
    s.env = { "HOME" => vagrant_home, "PROJECT_DIR" => project_directory }
  end

  config.vm.provision :shell, run: "always" do |s|
    s.name = "Bootstrapping development server"
    s.path = "scripts/bootstrap.sh"
    s.args = [ project_directory ]
  end

  config.vm.network :forwarded_port, guest: 1936, host: vm_config["haproxy_port"]
  config.vm.network :forwarded_port, guest: 8080, host: vm_config["web_port"]
  config.vm.network :forwarded_port, guest: 4200, host: vm_config["angular_port"]
  config.vm.network :forwarded_port, guest: 5432, host: vm_config["db_port"]
  config.vm.network :forwarded_port, guest: 6379, host: vm_config["queue_port"]
  config.vm.network :forwarded_port, guest: 8089, host: vm_config['locust_port']
end
