
# Discovery static assets

**<** [Application Data](data.md) | **^** **[Architecture Overview](readme.md)**

<br/>

## Asset Types

In the Discovery application, currently all static assets are grouped under the directory: [discovery_site/static/discovery_site](https://github.com/PSHCDevOps/discovery/tree/master/discovery_site/static/discovery_site)

There are currently four types of static assets served to the client from the Django web application.

 1. **images** - _The Discovery image folder that contains various theme related imagery_
 2. **css** - _The central store for all Discovery related CSS files_
 3. **javascript** - _The central store for all Discovery related JS files_
 4. **capability_statements** - _Directory of vendor capability statements that are available for download_

<br/>

## Generating static assets

All static assets are served from the individual web servers.  Upon deployment on the web application cluster, the static files are transferred to a top level **static** directory that is available over the internet.

#### Static asset generation scripts

```bash
# Collect all static files into the top level static directory
#  - This is run on every web container deployment before the site starts up
$ scripts/init-webserver.sh # No options
```

<br/>

## Asset generation / collection triggers

Asset collection into the top level project directory happens before every web container deployment.

<br/>
