
## General System Description

### System Purpose and Function

The GSA Discovery application is a tool that helps contracting professionals and other interested parties conduct market research on GSA contract vehicles and their suppliers. Users can search for available vendors by contract and NAICS code.  The results can be further filtered down by vendor set-aside classifications.  While the current version of Discovery is somewhat limited in vendor scope and available data, this system is expected to evolve to encompass a wide range of contracting vehicles and vendor related information.

The goal of Discovery is to provide acquisition professionals the means to research various contract vehicles while research historical information and vendor availability related to their particular acquisition need in order to reduce contract duplication by encouraging the use of existing vehicles through transparency.


#### Discovery Data

Currently there are two primary acquisition vehicles encompassed within the Discovery ecosystem; OASIS Small Business, and OASIS Unrestricted.  There are more vehicles planned in the near future which will add more vendors serving more NAICS codes.  There are currently a total of six vendor pools from the two vehicles currently offered.  Over time the vendor pools will grow with the addition of new vehicles.

Vendor information is loaded from a combination of information gathered from PSHC staff collected into spreadsheets and SAM registration information pulled from the SAM API.  The pool information that is collected by GSA PSHC staff is loaded from source files in the code base and do not change often.  The SAM is continuously checked for updated information.

Discovery collects basic information on contract awards and modifications by vendors in the aforementioned vendor pools.  This information includes the NAICS classification, transaction amount, and other information such as employee count and company revenue at that point in time if available.  In the future the actual data collected from contracts might change or grow.  The contract information is currently pulled from the GSA FPDS API and is continuously updated to ensure that fresh contract information can be factored into market research being performed. Currently, Discovery displays 10 years worth of historical data by vendor and NAIC.


#### Discovery Functions

Discovery is a simple application by design.  You can use the system in one of two ways; collect information from the vendor and contract focused API, or browse the website to see quick displays of information related to contracts being processed by included vendors.  The frontend user centered display is generated from data pulled from the backend API.

The Discovery API is a simple data pull system that allows users to request information on vendors, contracts, and NAICS codes.  In the future as more data is added the breadth and depth of these APIs will likely grow to serve the new data.

The Discovery frontend is a Javascript centric rendering and filtering interface designed to allow the user to filter down a set of vendors serving a particular NAICS code, possibly using set-aside filters.  The vendor information returned includes links to a vendor page, as well as information about the contracts that the vendor has executed within the supported vehicles for that NAICS code.  There are plans to re-envision the interface to provide more comprehensive and flexible displays, as well as advanced search and filtering.

To keep all of the vendor and contract data current automated scheduling of tasks is performed through background “worker” processes.  The Discovery website provides a means for configuring the timing and optional parameters for these regular content updates.  To update the schedule of the periodic updates from FPDS and SAM APIs administrative users need to login and will have access to a simple administrative information for creating schedules for tasks and viewing task execution results.


#### Discovery Links

_Production Link_: https://discovery.gsa.gov  (https://discovery.app.cloud.gov)
_Staging Link_: https://discovery-dev.app.cloud.gov
_Git Repository_: https://github.com.com/PSHCDevOps/discovery


### Discovery Components and Boundaries

The GSA Discovery application is a Python Django application that relies on open source technologies and ATO’d hosting technologies to provide a public repository of searchable acquisition related information.


#### Application components

Discovery consists of a group of interrelated Python Django applications that rely on external services for data storage, tasks queuing, session storage, and data ingestion.  All of these systems with the exception of external data API sources are housed internally within the Cloud.gov environment.

The Python Django application relies upon a connection to a PostgreSQL database that contains all of the primary application related data.  All data loaded from external sources gets stored and retrieved from this database.  Currently we use the aws-rds Cloud.gov service to provide this database.  This database contains tables pertaining to administrative users and related information, system state information, cache tables, vendor information, and contract data.

In order to continuously update the data in the Discovery system, a scheduler and workers are constantly running (in a service like Cron).  This service relies upon both the PostgreSQL database used by the primary Django application, and a Redis queue for collecting background tasks for processing that are deposited in the queue by the scheduler.

To scale the Discovery application to multiple web servers with the possibility of administrative login we need to maintain our user session information in an external data store.  For this, we use another Redis instance that contains all of our session data that is shared across all available web servers.

The Django Discovery application has three primary architectural components; API, frontend Javascript site, and data loaders.  The data loaders are commands embedded in the application that retrieve all of the data displayed in the Discovery application.  The API builds on the loaded data to provide endpoints for accessing the information.  Finally the Javascript application renders acquisition related data from the API’s into a user friendly format, and allows for filtered queries.


#### Application hosting

The networking boundaries for the Discovery system are contained fully within the ATO’d Cloud.gov architecture with the exception of external public data sources covered in the next section.  The Cloud.gov architecture consists of a group of applications, services, and routes that contribute to a fully functioning system.  There is no physical hardware required for the continued operations of the Discovery application.

There are two persistent spaces within the Cloud.gov Discovery organization that contain both a development staging environment and a live production environment.  Each of these spaces is configured exactly the same with the exception of the number of servers of a given type currently operating, and a CDN service tied to the production Discovery domain that maps to a web application cluster.  There may be other temporary application spaces created and destroyed as necessary to test various features and bug fixes in the hosting environment.


##### Cloud.gov services

Each Cloud.gov space contains five separate services needed to power the Discovery application.  All configurations and naming conventions are the same across all spaces.

**Service account** _(with deployment key)_ - A service that provides a temporary account, username, and password that allows our CI/CD system (CircleCI) to deploy the application to the space.  By default development and production spaces have them to facilitate GitHub merge based deployments, but other temporary spaces may be configured with them as needed for testing purposes.

**PostgreSQL AWS-RDS** _(single database)_ - The primary data store for the Discovery application.  For a more detailed overview, see the Application components section above.

**Redis 3.2** _(single database)_ - A session store for multi web server authentication of the Django web application.  For a more detailed overview, see the Application components section above.

**Redis 3.2** _(single database)_ - A queue for storing background tasks to be completed.  For a more detailed overview, see the Application components section above.

**Application configuration variables** - A user provided service that stores the values of four environment variables; API_HOST, API_KEY, SAM_API_KEY, and SECRET_KEY.  These environment variables are shared (or bound) to all web, scheduler, and worker servers in the space.

**CDN service** _(production space only)_ - A custom domain, AWS Cloud Front CDN, and HTTPS certificate configuration for the production site at https://discovery.gsa.gov


##### Cloud.gov applications

The Discovery web application cluster are Cloud.gov servers built on the commonly used Cloud Foundry Python buildpack.  All of our deployed applications use the Django web framework, so build the same dependencies from top level requirements files.

**Discovery Web** - The frontend Discovery website and API layer.  In each of the development and production spaces we maintain a cluster of at least two application servers running behind the Cloud.gov load balancer.

**Discovery Scheduler** - A Django Celery Beat based scheduling service that continuously runs in the background sending background tasks for Worker servers periodically, as configured through the Django administrative interface.  Only a single Scheduler server should be running in the Cloud.gov space.

**Discovery Worker** - A Django Celery background task processing service that continuously runs processing tasks created from the Scheduler or the application code.  Currently only the Scheduler creates background tasks for Worker servers but this may change in the future.  Depending on the space and volume of tasks, multiple Worker servers may be running in the Cloud.gov space.


##### Cloud.gov routes

Every space contains one preconfigured route from the application manifests that points to the Cloud.gov load balancer that routes traffix to the Discovery web servers.  This route hostname is different on all spaces.


#### Data sources

##### Vendor pool CSVs

The Discovery application loads vendor information from various CSV files committed into the application source code.  This data is updated as information changes with software releases.


##### SAM vendor registrations

The Discovery application reaches out and pulls publicly available vendor registration information from the SAM API.  This API requires a Data.gov API KEY but otherwise has no security restrictions.


##### FPDS contract awards and modifications

The Discovery application reaches out and pulls publicly available vendor contract awards and modifications from the FPDS API (ATOM feed).  This API does not require any type of API key and has no real security restrictions.
