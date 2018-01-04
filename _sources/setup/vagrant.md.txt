
# Discovery on Vagrant

**<** [Getting Started](getting_started.md) | **^** **[Setup Overview](readme.md)** | [Docker Setup](docker.md) **>**

## Installation

Vagrant installation is very easy.  It requires two things; a Virtual Machine provider, and the Vagrant application.

Discovery comes packaged currently for Virtualbox so you will need to have Virtualbox installed.  See the Virtualbox install instructions below to install for your operating system.  They have an installer for most operating systems.

1. **Virtualbox** - Install Virtualbox from: https://www.virtualbox.org/wiki/Downloads

Vagrant is available as an executable installer for Windows, Mac, and Linux.

2. **Vagrant** - Install Vagrant from: https://www.vagrantup.com/downloads.html


## Configuration

The Discovery Vagrantfile is meant to be configurable depending on the needs of the developer.  To keep everything that needs to be versioned, we use a pattern of a default Vagrant configuration file that can be overridden if an override exists.

You will also need to ensure certain environment variables are set for the Discovery application containers.  We provide an example ([docker/django-env.example.vars](https://github.com/PSHCDevOps/discovery/blob/master/docker/django-env.example.vars)) but you will need to create a file called **docker/django-env.vars** that has sensative application information.

```bash
# Fetch Discovery project
$ git clone https://github.com/PSHCDevOps/discovery.git {project_directory}
$ cd {project_directory}

# vagrant-config.yml is ignored by Git so your configurations will not be versioned
$ cp vagrant-config.default.yml vagrant-config.yml

# docker/django-env.vars is ignored by Git so your configuration will not be versioned
$ cp docker/django-env.example.vars docker/django-env.vars
```

_See the sections below for notes on the available configurations..._


### Vagrant configurations

 * **server_name** _default: discovery-dev_

    Sets the internal hostname of the virtual machine.

 * **ip_address** _default: system assigned_

    Sets the host ip address by which the virtual machine can be reached.  If this is not set then the system automatically selects an available IP.  Set this if you need to ensure the virtual machine is listening at a particular address.

 * **box_name** _default: ubuntu/trusty64_

    Sets the box or image to use from the [Vagrant Cloud](https://app.vagrantup.com/boxes/search) marketplace.

 * **cpus** _default: 2_

    Sets the number of virtual CPUs that should be used for the virtual machine.

 * **memory_size** _default: 2048_

    Sets the memory allocation for the virtual machine.  You may need to increase this depending upon how you load data.

 * **web_port** _default: 8080_

    Sets the host port for the Discovery web site.  By default this is 8080 and should not be changed unless you really need to and you know what you are doing.  Discovery Javascript receives an environment variable with the host and port to connect to to fetch data from the API.  If these do not align then there can be issues with the front end display.

    If this is changed, the **API_HOST** environment variable should also be updated in the **docker/django-env.vars** file covered in the [next section on Docker setup](docker.md).

 * **db_port** _default: 5432_

    Sets the host port that the cluster PostgreSQL database is available.  This is handy for connecting with the Docker database from the host machine through a [client command](https://www.postgresql.org/docs/10/static/reference-client.html) or through a graphical management interface like [DBeaver](https://dbeaver.jkiss.org/)

 * **queue_port** _default: 6379_

    Sets the host port that the Redis queue is available.  This is handy if you already have tools for inspecting the queue on the host machine.

 * **copy_ssh** _default: false_

    Whether or not to share the host user **.ssh** information (_except the authorized_hosts file_) with the Vagrant virtual machine.  This is handy if you want to be able to push to remote repositories requiring SSH keys.  If this is shared the Docker environment will share with all of the Django containers, giving you pass through push ability of protected repositories.

 * **copy_gitconfig** _default: true_

    Whether or not to share the host user **.gitconfig** file with the Vagrant virtual machine.  This is handy if you want to be able to commit without resetting this information within the development environment.  If this is set, this file is shared with all Django containers giving you a consistent identity across the host, development machine, and application containers.

 * **copy_vimrc** _default: false_

    Whether or not to share a host user VIM editor configuration with the Vagrant virtual machine.  This can be useful if you use VIM for inspecting files.  If this is set it is shared with all Django Docker containers.

 * **copy_profile** _default: false_

    Whether or not to share the host user Bash **.profile** with the Vagrant machine.  This can allow you to align your environment more closely with your host environment if you use a Bash based shell (on a Mac or Linux).  If this is set it is shared with all Django Docker containers.

 * **copy_bash_aliases** _default: false_

    Whether or not to share a host user Bash **.bash_aliases** file with the Vagrant machine if it exists.  Sometimes this file can define handy aliases sourced into the **.bashrc** so we give a change to share with Vagrant and the Django containers as well.

 * **copy_bashrc** _default: false_

    Whether or not to share the host user Bash **.bashrc** script with the Vagrant virtual machine.  This allows for a consistent environment across host, development machine, and application containers.

    Note that the contents of the [scripts/vagrant-bash.sh](https://github.com/PSHCDevOps/discovery/blob/master/scripts/vagrant-bash.sh) script are appended to any shared **.bashrc** or the default box provided one during the Vagrant provision process.


### Application configurations

 * **API_HOST** _default: http://localhost:8080_

    Sets the API request location for the Discovery frontend. The Discovery application passes the host and port of the API interface to the frontend Javascript.  This enables the Javascript to make requests to the API which basically power the frontend displays.  If no data is loading in the interface, chances are that this value is wrong.

 * **API_KEY** _default: **REQUIRED!!!**_

    Sets a [Data.gov API key](https://api.data.gov/signup/) that is passed to the Discovery API by the frontend Javascript.

 * **SAM_API_KEY** _default: **REQUIRED!!!**_

    Sets the [Data.gov API key](https://api.data.gov/signup/) that is passed to requests to get SAM vendor registration information.

 * **SECRET_KEY** _default: **REQUIRED!!!**_

    Sets a secret alpha-numeric key that is required by Django for certain operations.  This key can be anything you like but it should be lengthy and randomistic.


## Running the virtual machine

```bash
$ cd {project directory}

# Start up and provision the Vagrant virtual machine using the packaged Vagrantfile
$ vagrant up

# SSH into the Vagrant virtual machine to start working with the application cluster
$ vagrant ssh
```

You are now in the shared project directory: **/vagrant**

When the Vagrant machine is first created all Docker containers specified in the docker-compose configuration are created and started.  The Discovery application cluster consists of a **Django web site**, a **Celery scheduler**, a **Celery worker**, **PostgreSQL database**, and **Redis queue**.

* **/vagrant** live at **localhost:8080** (_if you didn't change **web_port** configuration_)

* **http://localhost:8080/admin**

  * First user: **admin**
  * Password:   **admin-changeme** (_please change!_)

<br/>

Using Vagrant, when SSHing into the virtual machine, you will be automatically redirected to the project root directory (**/vagrant**) and **docker-compose up** will be run to ensure Docker application containers are up to date.

**Git**, **Cloud Foundry Client** with the **Autopliot plugin**, **Docker**, and **Docker Compose** come installed on the Vagrant virtual environment initially.  The development environment is meant to bundle tooling necessary to running the Discovery application that might not make sense to install in the containers, and it provides a platform for running isolated Docker clusters in Docker Compose.


## Common Vagrant commands

* Run from the **host** machine
* Run from the **top level project** directory

```bash
$ vagrant status       # Check the status of the virtual machine

$ vagrant up           # Create a new or run an existing virtual machine
$ vagrant provision    # Re-provision development environment from specs in Vagrantfile
$ vagrant ssh          # SSH into a running virtual machine

$ vagrant halt         # Stop and save an existing virtual machine
$ vagrant destroy      # Completely destroy an existing virtual machine
```

More on the available [vagrant commands](https://www.vagrantup.com/docs/cli/)


## Getting help

If you run into issues please [file an issue](https://github.com/PSHCDevOps/discovery/issues) if you can not get it resolved through Vagrant documentation or help channels.  Vagrant has pretty [comprehensive documentation](https://www.vagrantup.com/docs/index.html) available and there are plenty of tutorials available covering pretty much all aspects of Vagrant usage.  Being an open source project there is a lot of discussion and question/answers related to Vagrant.

There is a [Vagrant Google group](https://groups.google.com/forum/#!forum/vagrant-up) you can join and you can chat with folks about Vagrant on [Gitter](https://gitter.im/mitchellh/vagrant).
