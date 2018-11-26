
# Discovery on Docker

**<** [Running with Vagrant](vagrant.md) | **^** **[Getting Started](readme.md)** | [Application setup](setup.md) **>**

<br/>

## Installation

Docker installation is fairly easy.  Our use of Docker requires two systems; the core Docker server, and Docker Compose for orchestrating container clusters.  Docker Compose makes it easy to work with projects containing many interlocking systems.

If you are using the Discovery Vagrant development environment you do not need to install Docker and Docker Compose.

1. **Docker** - Install Docker from: [https://www.docker.com/community-edition](https://www.docker.com/community-edition)
              _- If running Debian or Ubuntu, you can install by running the [scripts/setup-docker.sh](https://github.com/PSHCDevOps/discovery/blob/master/scripts/setup-docker.sh) script_


2. **Docker Compose** - Install Docker Compose from: [https://docs.docker.com/compose/install](https://docs.docker.com/compose/install)
                      _- This is included in the [scripts/setup-docker.sh](https://github.com/PSHCDevOps/discovery/blob/master/scripts/setup-docker.sh) setup_

<br/>

## Configuration

You will need to ensure certain environment variables are set for the Discovery application containers.  We provide an example ([docker/django-env.example.vars](https://github.com/PSHCDevOps/discovery/blob/master/docker/django-env.example.vars)) but you will need to create a file called **docker/django-env.vars** that has sensitive application information.

```bash
# Fetch Discovery project
$ git clone https://github.com/PSHCDevOps/discovery.git {project_directory}
$ cd {project_directory}

# docker/django-env.vars is ignored by Git so your configuration will not be versioned
$ cp docker/django-env.example.vars docker/django-env.vars
```

_See below for notes on the available configurations..._

<br/>

### Application configurations

 * **API_HOST** _default: http://localhost:8080_

    Sets the API request location for the Discovery frontend. The Discovery application passes the host and port of the API interface to the frontend Javascript.  This enables the Javascript to make requests to the API which basically power the frontend displays.  If no data is loading in the interface, chances are that this value is wrong.


 * **SAM_API_KEY** _default: **REQUIRED!!!**_

    Sets the [Data.gov API key](https://api.data.gov/signup/) that is passed to requests to get SAM vendor registration information.


 * **SECRET_KEY** _default: **REQUIRED!!!**_

    Sets a secret alpha-numeric key that is required by Django for certain operations.  This key can be anything you like but it should be lengthy and randomistic.

 * **GA_TRACKING_ID** _default: **None**_

    Sets a Google Analytics tracking id for the environment.  This is fed into the frontend HTML tracking snippet in the Discovery template.

<br/>

## Running the Docker services

```bash
$ cd {project directory}

# Ensure all Docker services are up to date and running if possible
$ docker-compose up -d

# You can verify all Docker services are running with
$ docker-compose ps
#
# You should see 5 containers running
#   1 web server
#   1 scheduler
#   1 worker
#   1 PostgreSQL database
#   1 Redis instance (tasks)

# "SSH" into a Docker container and have a look around
#
# full-container-name = {network}_{name}_{instance_num}
#
# ex;  discovery_web_1
#      vagrant_worker_1
#
$ docker exec -it {full-container-name} bash

# Build frontend Angular application
$ scripts/build-frontend.sh

# Wait for database migration to complete (should see "beat: Starting")
$ docker-compose logs --follow scheduler

# Load data fixtures if migration complete
$ scripts/load-fixtures.sh
```

You are now in the shared project directory: **/discovery**

* **/discovery** live at **localhost:8080**

<br/>

## Common Docker commands

* Run on either the **host** or **vagrant** machine (_if installed and used_)
* Run from the **top level project** directory

```bash
$ docker-compose ps                      # List all running containers from the docker-compose images

$ docker-compose logs web                # Display recent log entries from the discovery_web_1 container
$ docker-compose logs -f web             # Follow log entries from the discovery_web_1 container

$ docker exec -it discovery_web_1 bash   # "SSH" into the running discovery_web_1 container

$ docker-compose up -d                   # Create and run all site containers/services in the background
$ docker-compose build                   # Rebuild docker images for all docker-compose services
                                         # - run "docker-compose up -d" after to update running services

$ docker-compose stop web                # Stop the Discovery web service
$ docker-compose rm web                  # Remove the Discovery web service
```

More on the [docker commands](https://docs.docker.com/engine/reference/commandline/cli/)

<br/>

## Getting help

If you run into issues please [file an issue](https://github.com/PSHCDevOps/discovery/issues) if you can not get them resolved through Docker documentation or help channels.  Docker has pretty [comprehensive documentation](https://docs.docker.com/) available and there are plenty of tutorials available covering pretty much all aspects of Docker usage.  Being an open source project there is a lot of discussion and question/answers related to Docker and Docker Compose.

Docker maintains [forums](https://forums.docker.com/) you can discuss Docker related issues and there are many groups that meet to support those trying to dig deeper into the world of containerization.

<br/>
