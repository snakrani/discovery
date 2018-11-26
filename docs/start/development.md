
# Discovery development options

**<** [About Discovery](about.md) | **^** **[Getting Started](readme.md)** | [Running with Vagrant](vagrant.md) **>**

<br/>

## Overview

So you've decided to try running your own copy of Discovery to play around with or contribute.  Great!  This document will walk you through the high level process of getting up and running with Discovery locally and point you in the direction of more specific information you might need during the process.

You should find development through either of two options easy and straight forward.  If you encounter problems during setup, or while managing your development environment, please [file an issue](https://github.com/PSHCDevOps/discovery/issues) and we will do our best to help troubleshoot.

<br/>

## Development options

You have two options when setting up the Discovery project locally; Docker within a [Vagrant](https://www.vagrantup.com/) virtual machine or [Docker](https://www.docker.com/what-container) running locally on the host through [Docker Compose](https://docs.docker.com/compose/overview/).  Each of these options has various pros and cons.  Here is a walkthrough of the characteristics of each strategy and ideal times to use one over the other.

Ultimately the Discovery application delivery architecture is built on Docker for local development and CI/CD and buildpacks for remote hosting, so Docker will be a necessity either way you choose.  In the future Cloud Foundry buildpacks will be replaced with Docker images, aligning local development, continuous integration and testing, and production application infrastructure.

<br/>

### 1. Vagrant development environments

Vagrant has been a popular choice for many years in providing standardized development environments between teams.  It works well on Windows, Mac, and Linux, and is easy to install and configure.  It requires a virtualization technology, such as Virtualbox or VMWare, to create the underlying virtual machines.  So in essence Vagrant is pretty much a command line wrapper, package integrator, and configuration interface for virtual machine providers.  Virtualbox is commonly used and is the standard due to the fact that it is relatively easy to setup and free to download and use.

The Vagrant development environment that ships with the Discovery project is a simple development machine designed to work with Git, Cloud Foundry, and Docker/Docker Compose to manage the Discovery application cluster, hosting environment, and Git project.

While running Vagrant is not necessary because Docker comes in various OS installers it does provide some handy features which make it a useful tool in the development process.  Using Vagrant is the recommended option for all developers contributing regularly on the project, so we can standardize working environments.

###### Vagrant Pros

 * Allows for clean separation of all project files and Docker related images, volumes, and containers
 * Provides a standardized development setup and tooling that other developers don't have to configure
 * Can destroy and rebuild entire Docker environment and caches in two simple commands
 * Do not have to worry as much about port collisions on the host system as clusters of Docker containers can be temporarily halted
 * Easier resource management on the host machine

###### Vagrant Cons

 * Slower than running Docker on the host machine
 * Vagrant boxes take up valuable space on the local hard drive
 * Provide an extra layer of complexity if you only use Docker

<br/>

It is best to use Vagrant over local Docker if you value complete isolation between Docker based projects, like to tightly manage resources and port mapping on a usually minimal desktop environment, are new to Docker and/or Cloud Foundry and don't want to worry about installing the development dependencies, or because you just like working with Vagrant.

If you are interested in learning more about how to set up the Discovery project with Vagrant then head on over to the [Vagrant guide](vagrant.md) to start getting Vagrant running and the Discovery project building on your machine.  The process should not take long.

<br/>

### 2. Docker running locally

Running Docker locally can have it's advantages in speed and reduction in complexity if you already run Docker and Docker Compose locally, usually on Mac or Linux.  It is also probably advantageous to have a clear process for keeping Docker related project artifacts easily separated.  If this is a minimal development desktop that is not used for multiple projects then using Docker locally can make sense.

At the root of the project directory is a Docker Compose configuration that can be used to spin up the five node cluster that is the Discovery application currently.

###### Local Docker Pros

 * Running Docker locally can be very fast
 * Docker takes up considerably less memory and diskspace than Vagrant
 * Eliminates another technology to install and manage
 * Less potential for resource sharing issues

###### Local Docker Cons

 * Docker containers and other resources from multiple projects are harder to manage in one workspace
 * High probability of port collisions (particularly for service ports)
 * Grew out of Linux container technology and still works best in that environment
 * You have to install Docker and the CF CLI and related plugins (easy to do with bundled scripts)
 * Harder to clear image and volume caches and start fresh when needed

<br/>

It is best to use local Docker over Vagrant if you use Docker in a minimal desktop environment that does not have clashing Docker projects to manage, if Vagrant is not a technology you want to install and update periodically, if you have very little in processing, memory, or harddisk resources on your machine, or if you already have your own flow with local Docker.

If you are interested in learning more about how to set up the Discovery project with local Docker then head on over to the [Docker guide](docker.md) to start getting Docker running and the Discovery project building on your machine.  This process should also not take long.

<br/>

## Getting help

If you run into problems along the way submit an issue in our [issue queue](https://github.com/PSHCDevOps/discovery/issues) and we will do our best to help out.

<br/>
