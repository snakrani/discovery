
# Discovery deployment process

**<** [Testing Processes](testing.md) | **^** **[Process Overview](readme.md)** | [Discovery Management](management.md) **>**

<br/>

## Deployment locally

The Discovery application system is easy to run locally on your own machine provided you have an active internet connection to download dependencies during setup.

You can either install locally through [Vagrant](../start/vagrant.md) or directly run the [Docker](../start/docker.md) cluster on your machine.  To get started running Discovery locally, check out the [Discovery getting started guide](../start/readme.md).

<br/>

## Deployment on CircleCI

Deployments to the development staging and production environments should only be made through the CircleCI platform.  This ensures that all updates flow through our Git branching and review process, which should lessen the change of cataclysmic catastrophe _(hopefully)_.

All deployments executed in the CircleCI CI/CD platform are defined within the configuration in the **.circleci** directory.

See the [Discovery setup guide](../start/setup.md) for more information on deployment related commands used by CircleCI.

<br/>
