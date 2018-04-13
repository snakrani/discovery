
# Discovery testing process

**<** [Development Processes](development.md) | **^** **[Process Overview](readme.md)** | [Deployment Process](deployment.md) **>**

<br/>

## Code evaluation

Currently there are no code evaluation tools in use within the Discovery application.  As soon as a suitable tool is chosen it will be integrated into the development environment and CircleCI CI/CD configuration for manual and automated testing.

All updates are reviewed however by maintainers and/or the Discovery management team before being merged into the staging branch, giving us the chance to catch glaring errors, omissions, or formatting issues during the life of the pull request.

<br/>

## Unit testing

The Discovery application currently implements unit testing for three Django application components; **API**, **vendors**, and **contracts**.

 1. **API** unit tests

    Take fixture data bundled with the application source code and run tests against the API endpoints checking for proper result data given specified inputs.

 2. **Vendor** unit tests

    Run various tests related to loading data from remote sources, vendor information checks, and capability statements.

 3. **Contract** unit tests

    Run various tests related to loading data from remote sources, and in the near future contract information checks.

<br/>

More unit testing coverage is needed to fully leverage the unit testing framework.  Areas that need special attention include the Vendor and Contract application components.

To learn more about executing Discovery unit tests see testing section of the [Discovery setup guide](../start/setup.md)

<br/>

## Acceptance testing

The Discovery application currently implements [Selenium](http://www.seleniumhq.org/) based acceptance testing through the [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started) library.  This library is installed by default on the Discovery Docker image and Vagrant development environment.

Acceptance testing requires a Discovery application server running at http://localhost:8080

To learn more about executing Discovery acceptance tests see testing section of the [Discovery setup guide](../start/setup.md)

<br/>

## Testing on CircleCI

All testing performed in the CircleCI CI/CD platform is defined within the configuration in the **.circleci** directory.

Currently we run unit tests and acceptance testing on all pushes or merges to branches on the official source repository.  Due to security issues CircleCI jobs are not available on pull requests from external forked repositories.

<br/>
