
# Discovery static assets

**<** [Application Data](data.md) | **^** **[Architecture Overview](readme.md)**

<br/>

## Asset Types

In the Discovery application, currently all static assets are grouped under the directory: [app/discovery/static/discovery_site](https://github.com/PSHCDevOps/discovery/tree/master/app/discovery/static/discovery_site)

There are currently four types of static assets served to the client from the Django web application.

 1. **images** - _Discovery image folder that contains various API docs theme related imagery_
 2. **css** - _A store for Discovery API docs related CSS files_
 3. **capability_statements** - _Directory of vendor capability statements that are available for download_

<br/>

## Generating static assets

All static assets are served from the individual web servers.  Upon deployment on the web application cluster, the static files are transferred to a top level **app/static** directory that is available over the internet.

#### Static asset generation scripts

```bash
# Collect all static files into the top level static directory
#  - This is run on every web container deployment before the site starts up
$ scripts/init-webserver.sh # No options

# Build Angular JS related assets and source files for web service
#  - This is run on every environment deployment before the site starts up
$ scripts/build-frontend.sh # No options
```

<br/>

## Asset generation / collection triggers

Asset collection into the top level project directory happens before every web container deployment.

<br/>
