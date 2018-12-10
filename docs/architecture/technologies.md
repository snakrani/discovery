
# Discovery technologies

**^** **[Architecture Overview](readme.md)** | [System and Interface Design](design.md) **>**

<br/>

## Dockerized development

It has long been a dream of developers, administrators, and other involved in the application creation process to avoid having discrepencies in the various operating environments hosting the applications, which can often cause lengthy delays in delivering the services to stakeholders due to potential troubles diagnosing issues.  It is also increasingly common now to host on scalable resources, which require a different mode of thinking about providing application services than the historical server as an asset model.

Containers and the Docker engine allow us to reach for the goal of a unified architecture across development, continuous integration and deployment, and production hosting environments.  Docker provides a lightweight application packaging system through layered images, and a dynamic runtime that is the core of many emerging scalability technologies.

### Benefits that Docker provides

 1. **Portability across machines**

    All application dependencies can easily be bundled into layered images that are easy to create, extend, and run collectively through technologies like Docker Compose, Kubernetes, and Cloud Foundry.

 2. **Extremely lightweight execution environment**

    Docker container images are very small compared to virtual machine images and take considerably less time to provision than systems built on configuration management systems, such as Puppet, Chef, and Ansible.  Configuration management systems can still be used to provision containers, but the Docker image architecture provides a handy caching mechanism that can prevent unnessesary time consuming provisioning.  This makes spinning up and runnind larger Docker clusters very fast, which is good for productivity.

 3. **Easy to share images**

    Docker is the most popular Linux container packaging system and runtime environment out there.  Many technologies have sprung up to create a vibrant ecosystem, and it is easy to create image marketplaces and repositories that can be reused and extended by others.  This makes it easy to build off of established work of others and contribute back upstream when it makes sense.

 4. **Container images easy to version control**

    You can track successive versions of a container, and even deploy new images through CI/CD processes.  It is easy to rollback to previous versions of a container, inspect differences, and rebuild select parts of the image hierarchy depending on the changes found.  This makes it easy to audit all changes to the underlying infrastructure and pursue a fully automated deployment mechanism that can update the underlying dependencies in a _"smart"_ way.

### How we use Docker

We currently use Docker for local development through Docker Compose, a tool for creating easily managed clusters of Docker containers.  We then use the same base Debian Stretch container images in our CircleCI environment and build our dependencies through setup scripts, housed in the [scripts directory](https://github.com/PSHCDevOps/discovery/tree/master/scripts).  This ensures that our local development environments and continuous integration and deployment environments are exactly the same, and easier to debug should issues arise.

Right now for our hosted applications, we use [Cloud.gov](https://cloud.gov/) (built on Cloud Foundry) and use the popular Python buildpack, which gets installed on Cloud.gov managed base container images during deployment.  In the future, when we get access to a Docker image marketplace, we are going to switch to building and using Marketplace containers as our base images for local development, CI/CD, and remote hosting on Cloud.gov.  This will allow us to align all environments behind a common architecture through Docker images.

For information about getting started with Docker for Discovery, check out our [getting started guide](../start/docker.md).

<br/>

## Cloud Foundry hosting

We host the Discovery staging environment and production infrastructure on [Cloud.gov](https://cloud.gov/) to reap the benefits of a supported open source Platform as a Service with the compliance benefits of a FedRAMP JAB authorization, which lightens our paperwork to develop the application.

Cloud.gov is built on [Cloud Foundry](https://www.cloudfoundry.org/), which is a popular PaaS used by enterprises across the globe, large and small.  Cloud.gov allows us to focus on developing just the application and leaves the infrastructure development and maintenance to those best qualified to handle that task.

### Benefits that Cloud.gov provides

 1. **Easy to create controlled access services**

    Within Cloud.gov, with a simple command we can create the backend services we need, be they PostgreSQL databases, Redis servers, or even service accounts for CI/CD.  All services come with machine generated randomistic credentials that are easy to rotate when needed.  These services can easily be bound to the applications that depend on them.  This is handy for us since we have multiple types of applications running depending on the same backend services.

 2. **Easy to update applications**

    Pushing applications in a zero downtime deployment is easy with Cloud Foundry, and helps us focus on developing the meat of the application instead of troubleshooting deployment issues.

 3. **Easy user and access management across siloed application spaces**

    Cloud Foundry makes managing users and access easy and we can create test spaces to try out application features and updates that can not interfere with existing production and staging environments.  This allows us to sleep at night.

 4. **Supports Docker image based deployments**

    Although we are not taking advantage of this feature yet, the latest FedRAMP'd Cloud.gov hosting environment supports deploying applications from publicly available marketplace images.  As soon we we find a suitable Docker marketplace we will start taking advantage of this system to unify our infrastructure environments.


### How we use Cloud Foundry

We currently use Cloud.gov combined with a popular [Python Cloud Foundry buildpack](https://github.com/cloudfoundry/python-buildpack) to host both staging and production environments.  In each space we run multiple Django web servers, a Django Celery scheduler, some Django Celery task processors, with Redis and PostgreSQL services providing shared data stores for different purposes.

In the future, as mentioned above, we will be migrating from the current buildpack architecture for Cloud Foundry to the deployment of Docker images for all Cloud.gov applications.

For information about getting started with Cloud Foundry with Discovery, get access to a Cloud.gov account and organization capable of deploying applications with PostgreSQL and Redis, then check out the Deployment section in our [getting started guide](../start/setup.md).

<br/>

## CircleCI integration and deployment

We use a GSA approved CI/CD service called [CircleCI](https://circleci.com/) to perform automated testing, builds, and deployment to our various hosting environments.  CircleCI is nice because it allows us to build off of Docker to create specific runtimes that have just the tooling we need to execute our jobs.  The newer 2.0 architecture also provides an easy way to create workflows which are easy to visualize, update, and track over time.

### Benefits that CircleCI provides

 1. **Configuration language is pretty flexible**

    CircleCI provides a pretty comprehensive syntax for orchestrating jobs in their remote container environment.  When paired with the entry of environment variables with their project interface this creates a powerful layered system where we can create workflows that respond to different events on different branches without much redundant definition of jobs.

 2. **Support for Dockerized tasks**

    Version 2.0 of the CircleCI service depends on Docker to provide the runtimes for jobs executed.  This allows us to reuse our packaging for development to execute remote jobs based on events in our source repository.

 3. **Easy concurrency of unrelated jobs**

    CircleCI provides an easy means of running jobs in parallel with full dependency management.  This makes it easy to speed up the response of the CI/CD checks on pushes or merges to project branches.  We can have a development deployment that depends on unit testing and acceptance testing, which each run in parallel.  Combined with parallel deployment to the hosting environment, this makes CI/CD must quicker and easier to work with in higher volume settings.

### How we use CircleCI

Currently we make all deployments to our staging and production environments via CircleCI jobs run on merges to the **develop** and **master** branches.

We also have CircleCI run acceptance and unit tests on all pushes to branches in the official project source repository.

Finally, we use CircleCI to autogenerate our documentation site that you may be reading right now on pushes to a **docs** branch or merges to **master** branch.

<br/>

## Django web framework

[Django](https://www.djangoproject.com/) is a popular Python web framework that is flexible enough to provide capable API services and rudimentary Content Management System like features with a lightweight footprint.  Django is meant to providea pluggable architecture that is easy to extend to our needs.

### Benefits that Django provides

 1. **Python is one of the most popular programming languages and easy to learn**

    Building in Python allows us to tap into a potentially wide range of developer talent.  Python is known to be easy to learn for those new to programming, it is a high level language with a vibrant contributor community, and is a very versatile programing language; being used for everything from infrastructure automation, data analytics, and web application development.

 2. **Django is lightweight and fast**

    When you know exactly what you are trying to build, starting with a web framework makes sense over a more full featured (and often slower and more reesource intensive) CMS system.  Discovery is built in layers, starting with a lightweight API, a structural Python template and view layer, and a foundational Javascript application that uses the API to render the application according to the Python views and templates.  This system gives us just enough to provide the services while keeping our runtime small and fast.  This also allows us to scale horizontally with demand with limited resources available.

 3. **Django is extensible**

    It is relatively easy to hook into Django and add needed functionality.  Django builds off of the popular Model, View, Controller design pattern so it is easy for developers coming from other systems to understand the extension points and hit the ground running fast.

 4. **Django is secure**

    Django makes a point of building security into the architecture so we can rely upon a lot of that underlying logic.  Since Django has many eyes looking through the code constantly security issues can be identifies easier and updates integrated into the Discovery application in a timely manner.

### How we use Django

All of our web application servers, scheduling instances, and task processors are built on Django _(currently version 1.8)_.  We integrate other libraries into this system through two top level requirements files:

 1. [requirements.txt](https://github.com/PSHCDevOps/discovery/blob/master/requirements.txt)
 2. [requirements-dev.txt](https://github.com/PSHCDevOps/discovery/blob/master/requirements-dev.txt)

<br/>

## Celery task scheduling and management

[Celery](http://www.celeryproject.org/) is a distributed task processing system, and is the most popular and extensible task execution system for Django currently.  The system is widely supported and has many task queue and result reporting backends that are available.  This makes it ideal for Discovery so we can change underlying technologies in the future if we need to and still keep a standardized background task execution and scheduling interface.

### Benefits that Celery provides

 1. **Celery is extensible**

    Rather than being built for a single technology or type of user, Celery tries to create a more modular architecture that can be plugged into with different capabilities.  This allows us to extend our task processing and scheduling capabilities easier over time.

 2. **Celery is well documented and used frequently with Django**

    There is a large amount of documentation, examples, and discussion about the Celery system online.  We can tap into this knowledge to build our own capabilities.  Celery was first designed for Python web frameworks like Django and Flask, so it is easy to integrate into our system.  It also provides a handy administrative interface for scheduling tasks and viewing results _(alright it is not pretty, but it is somewhat functional)_

 3. **Celery is easy to scale as needed**

    Celery workers are easy to scale when needed with popular data queues, like Redis, which happens to be available in our Cloud Foundry hosting environment.

### How we use Celery

We use two primary Celery related systems; Celery workers that pull tasks from a Redis queue, and a [Celery Beat](https://github.com/celery/django-celery-beat) scheduler that queries periodic tasks set through the administrative interface.

<br/>

## PostgreSQL database

The [PostgreSQL database](https://www.postgresql.org/) is a popular choice with Django projects, and is widely used at [18f](https://18f.gsa.gov/), the original developers of this Django application.  It is also available within the Cloud.gov hosting environment and approved for use at GSA.

Since we do not write queries as much as access obect models through methods in the code, which translate queries, the syntax of the database is not as important to us as the availability, security, and performance of the underlying database engine.

### How we use PostgreSQL

In the Discovery application, we currently use the PostgreSQL database for all development, staging, and production databases required for Django operations.

<br/>

## Redis datastore

The [Redis datastore](https://redis.io/) is a popular structured in-memory data store that is commonly used as a object database, cache, and message broker.  It supports many data types, and is built for high traffic applications.  Redis is also used frequently at GSA, and is readily available within the Cloud.gov hosting environment, making it an easy choice for our object store and queueing needs.

### How we use Redis

We currently use Redis as a task queue for storing tasks for Celery task processing servers to fetch and execute jobs.  Celery workers are constantly pulling tasks from this queue, and our Celery Beat scheduler adds them periodically based on configurations in the administrative interface for periodic tasks needing to be run during normal operations.

<br/>
