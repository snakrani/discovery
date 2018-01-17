
# Discovery Setup

**<** [Discovery on Docker](docker.md) | **^** **[Getting Started](readme.md)**

<br/>

## User management

When up and running with the Discovery application, the first thing you will need to do is to ensure there is at least one administrative user for the system that can handle scheduling data update tasks in the system, and monitor their progress over time.

Both the local Docker environment and Cloud Foundry based buildpack deployments ensure an initial _super user_ with the username **admin**.  By default the password for this user is **admin-changeme**, but this can be reset through the administrative interface after logging in.  This account also has a dummy email by default, which should be changed.

_Note:_ The Discovery application does not currently send emails, so the user email entry is not currently used.

<br/>

### User related scripts

```bash
# Initialize the Django database and ensure an administrative user with the username admin
#
# This script is called on initialization of a new Django Celery Beat Scheduler, as there
# should only ever be a single Scheduler for a Discovery application cluster
#
$ scripts/init-db.sh  # Has no options

# Update or create an administrative user
$ scripts/create-admin.sh --help
```

<br/>

### User management interface

The user management interface can be found at: http://localhost:8080/admin/auth/user _(change port if different)_

![Discovery user management](https://raw.githubusercontent.com/PSHCDevOps/discovery/docs/docs/images/User-Management.png)

<br/>

## Data loading

After the site is running and you have an administrative user that can login, you need to populate the site with data.  For most purposes a limited set of data useful for debugging and development of new features is preferable to complete repositories of information spanning potentially 10 years or longer.

When running the Discovery application you have two options; load data from packaged fixtures, or load data directly from the remote APIs that provide the source data for the production Discovery system.

<br/>

### 1. Loading from packaged fixtures

 Pros                                            | Cons
 ----------------------------------------------- | -----------------------------
 Loading from fixtures is fast                   | Data loaded is not up to date
 Guaranteed to get same data as other developers | Incomplete data available
 Not very memory or resource intensive           | Does not test update process


#### Fixture related scripts

```bash
# Loads all fixture data into the Discovery application
$ scripts/load-fixtures.sh  # Has no options

# Generate new fixture data with the data currently in the Discovery application
$ scripts/gen-fixtures.sh  # Has no options
```

<br/>

### 2. Loading from remote APIs

 Pros                                                   | Cons
 ------------------------------------------------------ | --------------------------------------------------
 Control the data you want _(to some degree)_           | Loading from remote APIs can be slow
 Data is up to date and may have parity with production | Not good for standardized tests _(eg; unit tests)_
 Data is complete and authoritive                       | Harder for collaborative development
 Allows for testing of the update process               | Requires a stable internet connection

#### Data loading related scripts and commands

```bash
# Helper script that fetches all production time period data into the Discovery application
$ scripts/fetch-data.sh  # Has no options

# Load all classification information into Discovery (currently these are all local file based)
# - included in fetch-data.sh
$ manage.py load_categories  # Has no options

# Load all acquisition vehicle vendor information into Discovery
# - included in fetch-data.sh
$ manage.py load_vendors --help

# Load all contract awards and modification for all vendors in the Discovery database
# - included in fetch-data.sh
$ manage.py load_fpds --help
```

#### Scheduled data updates

The Discovery application is built to periodically check for updates from remote sources based upon a schedule determined by a site administrator.  All data can be loaded initially through this mechanism as well, which is useful for testing the update mechanism.

This Django application uses the well documented, extensible, and popular background task processor called [Celery](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html) and an addon scheduling application built on a Celery extension; [Celery Beat](http://django-celery-beat.readthedocs.io/en/latest/).  These libraries provide an administrative interface that allows us to change the periodic schedule of updates, and audit background task results.

To schedule content updates, navigate to: http://localhost:8080/admin/django_celery_beat  _(change port if different)_

_You will notice four sections:_

 1. **Crontabs** - Very flexible schedule built on the [Cron scheduling format](https://en.wikipedia.org/wiki/Cron)
 2. **Intervals** - Simple scheduling format with an interval and unit of time _(e.g., 3 days)_
 3. **Solar Events** - Scheduling based on position of sun in relation to earth at geo coordinates _(you probably won't need this)_

 ---

 4. **Periodic Tasks** - Management of scheduled tasks that use the periods scheduled above _(a task can only have one scheduling event)_


#### Task scheduling interface

The task scheduling interface can be found at: http://localhost:8080/admin/django_celery_beat/periodictask _(change port if different)_

![Discovery scheduling interface](../images/Task-Scheduling.png)

_Creating a new scheduled task that **updates contracts** at **10:05AM UTC** everyday_

![Discovery periodic task interface](../images/Periodic-Task.png)

You can check on the results of executed tasks at http://localhost:8080/admin/django_celery_results/taskresult _(change port if different)_

![Discovery task result interface](../images/Task-Results.png)

<br/>

## Testing changes



<br/>

## Deployment information



<br/>

## Documentation generation



<br/>
