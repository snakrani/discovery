
# Discovery management

**<** [Deployment Process](deployment.md) | **^** **[Process Overview](readme.md)** | [Contributing to Discovery](contributing.md) **>**

<br/>

## Logging

Locally all logs are stored and accessible in the **logs** directory.  On the Cloud.gov hosting environment all log entries collected can be filtered and displayed through a Cloud.gov hosted [Logstash / Kibana interface](https://logs.fr.cloud.gov).

We collect different types of logs in the Django application that can be found in the **discovery/settings.py** **LOGGING** variable.  For application operations we track normal Django events in an eventlog, for data loading we track source values, download events, and memory usage over time.  In Cloud.gov we track access to Discovery pages and general platform errors and issues.

<br/>

## Monitoring

We will soon be implementing New Relic for application level monitoring.

We currently track all application traffic through Google Analytics and report usage information to Digital.gov for tracking on https://analytics.usa.gov.

<br/>
