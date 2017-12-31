![Discovery image](https://discovery-dev.app.cloud.gov/static/discovery_site/images/discovery.png)

<br/>

| Branch       | Site        | CircleCI Status   |
| :---------   | :---------  | :-----------------|
| **Develop** | [discovery-dev.app.cloud.gov](https://discovery-dev.app.cloud.gov)  | [![CircleCI](https://circleci.com/gh/PSHCDevOps/discovery/tree/develop.svg?style=svg)](https://circleci.com/gh/PSHCDevOps/discovery/tree/develop) |
| **Master**  | [discovery.gsa.gov](https://discovery-dev.app.cloud.gov) | [![CircleCI](https://circleci.com/gh/PSHCDevOps/discovery/tree/master.svg?style=svg)](https://circleci.com/gh/PSHCDevOps/discovery/tree/master) |

<br/>

## Discovery overview

Discovery is a market research tool for GSA Contract Vehicles. Currently, it features GSA IDIQ vehicles, with more contracts coming in the future. Use Discovery to search vendor history for the awarded contractors and NAICs of the various IDIQs. Each contract is separated into Unrestricted and Small Business (SB) to make it easy to reserve task orders for small business categories.

## Documentation

All of Discovery's developer and maintenance documentation is located in the [docs](overview.md) directory.  To get started, you'll probably want to either read through the [Setup guide](setup/overview.md) or the [Architecture guide](architecture/overview.md), depending on your preference.

#### Getting set up with Discovery

* [**Setup and configuration overview**](setup/overview.md)
  * [About Discovery](setup/about.md)
  * [Getting Started](setup/getting_started.md)
  * [Running with Vagrant](setup/vagrant.md)
  * [Running directly with Docker](setup/docker.md)
  * [Application requirements](setup/requirements.md)

#### Discovery architecture and design

* [**Discovery architecture overview**](architecture/overview.md)
  * [Technologies required](architecture/technologies.md)
  * [System and interface design](architecture/design.md)
  * [Discovery data](architecture/data.md)
  * [Static assets](architecture/assets.md)

#### Discovery related processes

* [**Discovery process overview**](process/overview.md)
  * [Development processes](process/development.md)
  * [Testing processes](process/testing.md)
  * [Deployment process](process/deployment.md)
  * [Discovery management](process/management.md)
  * [Contributing to Discovery](process/contributing.md)

#### Useful links

* [Trello board](https://trello.com/b/AEoWtET7/discovery-20)
* [OASIS information](https://www.gsa.gov/acquisition/products-services/professional-services/one-acquisition-solution-for-integrated-services-oasis)

## Related projects

* [PyFPDS library](https://github.com/18f/pyfpds)
