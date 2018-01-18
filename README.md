![Discovery image](https://raw.githubusercontent.com/PSHCDevOps/discovery/master/discovery_site/static/discovery_site/images/discovery.png)

<br/>

| Branch       | Site        | CircleCI Status   |
| :---------   | :---------  | :-----------------|
| **Develop** | [discovery-dev.app.cloud.gov](https://discovery-dev.app.cloud.gov)  | [![CircleCI](https://circleci.com/gh/PSHCDevOps/discovery/tree/develop.svg?style=svg)](https://circleci.com/gh/PSHCDevOps/discovery/tree/develop) |
| **Master**  | [discovery.gsa.gov](https://discovery-dev.app.cloud.gov) | [![CircleCI](https://circleci.com/gh/PSHCDevOps/discovery/tree/master.svg?style=svg)](https://circleci.com/gh/PSHCDevOps/discovery/tree/master) |

<br/>

## Discovery overview

Discovery is a market research tool for GSA Contract Vehicles. Currently, it features GSA IDIQ vehicles, with more contracts coming in the future. Use Discovery to search vendor history for the awarded contractors and NAICs of the various IDIQs. Each contract is separated into Unrestricted and Small Business (SB) to make it easy to reserve task orders for small business categories.

<br/>

## Documentation

All of Discovery's developer and maintenance documentation is located in the [docs](docs/overview.md) directory.  If you are new to the Discovery application, you'll probably want to read through the [Getting Started guide](docs/start/readme.md) first.

The [Architecture guide](docs/architecture/readme.md) provides a high level summary of the application design and the data available, and the [Process guide](docs/process/readme.md) covers various development and administrative processes required for continued operations of the Discovery application.

All Discovery related documentation is available as a mobile friendly [documentation site](http://pshcdevops.github.io/discovery).

<br/>

#### Getting set up with Discovery

* **[Getting Started](docs/start/readme.md)**
  * [About Discovery](docs/start/about.md)
  * [Development options](docs/start/development.md)
  * [Running with Vagrant](docs/start/vagrant.md)
  * [Discovery on Docker](docs/start/docker.md)
  * [Application setup](docs/start/setup.md)

#### Discovery architecture and design

* **[Discovery architecture overview](docs/architecture/readme.md)**
  * [Technologies required](docs/architecture/technologies.md)
  * [System and interface design](docs/architecture/design.md)
  * [Discovery data](docs/architecture/data.md)
  * [Static assets](docs/architecture/assets.md)

#### Discovery related processes

* **[Discovery process overview](docs/process/readme.md)**
  * [Development processes](docs/process/development.md)
  * [Testing processes](docs/process/testing.md)
  * [Deployment process](docs/process/deployment.md)
  * [Discovery management](docs/process/management.md)
  * [Contributing to Discovery](docs/process/contributing.md)

#### Discovery security documentation

* [Discovery SSP reference](docs/files/Discovery-Controls-LATO.pdf)

<br/>

#### Useful links

* [Trello board](https://trello.com/b/AEoWtET7/discovery-20)
* [OASIS information](https://www.gsa.gov/acquisition/products-services/professional-services/one-acquisition-solution-for-integrated-services-oasis)

<br/>

## Related projects

* [PyFPDS library](https://github.com/18f/pyfpds)

<br/>

## License information

This source code and all related application assets are released under CC0 1.0 Universal public domain, with the exception of some libraries the Discovery application depends on.  See the [LICENSE](LICENSE.md) for more details.
