
# Discovery development process

**^** **[Process Overview](readme.md)** | [Testing Processes](testing.md) **>**

<br/>

## Version control and branching strategy

The Discovery application is managed through Git and hosted as a [source repository on GitHub](https://github.com/PSHCDevOps/discovery).  Certain libraries have also been forked to the [PSHCDevOps GitHub organization](https://github.com/PSHCDevOps) as needed to patch for the Discovery system.

### Branch / Hosting environment mappings

 * **master** branch maps to **production** hosting environment
 * **develop** _(default)_ branch maps to **staging** hosting environment
 * **gh-pages** branch is a special documentation site hosted on GitHub generated from this documentation
 * **docs** branch is an optional branch that can deploy documentation updates before production release

### Forking and development flow

All maintainers may work off of the official source repository in feature or hotfix branches derived from the **develop** branch, which can be pushed and tested before ultimately creating a pull request that gets merged into the **develop** branch when ready _(and reviewed if multiple developers working on project)_.  When **develop** is deployed to the [development staging environment](https://discovery-dev.app.cloud.gov/) and everything is reviewed and functioning properly, then **develop** can be merged into **master** triggering a production deployment.  Neither the **develop** or **master** branch can be pushed to directly by design.

All external contributors should fork the repository and create feature or hotfix branches derived from the **develop** branch.  When ready a pull request should be issued, which a maintainer can merge into a official repository test branch before merging into the **develop** branch.  The reason for creating an intermediate branch is that we can not expose CircleCI environment variables to non maintainers and we need to ensure all tests pass before merging from a feature or hotfix branch into **develop**.  Once the changes are merged to **develop**, the updates follow the same develop process as defined above for maintainers.

Currently deployments to production may be made anytime an update is ready to deploy.  This **"may"** get a little more structured in the future.  We want to encourage fast deployments to the production system though instead of manufacturing delays in the process.

<br/>

## Issues and pull requests

All external contributors, end users, and maintainers are encouraged to file issues in the [Discovery issue queue](https://github.com/PSHCDevOps/discovery/issues) and/or create pull requests on the official source repository with suggested updates and fixes.

Pull requests should be clearly defined and follow general Discovery application conventions unless attempting to replace a convention throughout the application codebase.  Any pull requests not meeting these criteria will be delayed or rejected.

<br/>

## Merges and deployments

All deployments to production and staging environments are expected to be the result of a CircleCI job, so there should be no manual deployments to either environment.  Staging deployments are triggered by merges to the **develop** branch, and production deployments are triggered by merges to the **master** branch.  Outside of testing, manual deployments are bad!

It may be necessary to create temporary test Cloud.gov spaces using the **scripts/setup-cf-space.sh** script, but this should not affect the production or staging application hosting environments.  This would also require more Cloud Foundry resources, which may not be available on the hosting environment.

All pull requests to the **develop** branch will be reviewed by the Discovery management team and current application maintainers.

<br/>

## Quality assurance

All updates to the Discovery application should be made and tested _(unit and acceptance)_ in isolated branches, which can then be merged on success to the **develop** branch, and **ONLY** the **develop** branch.  All merges to **master** should be from **develop** branch updates _(which is why the develop branch is the default branch)_.

This process enforces a review process before ending up in the production environment which can help us catch bugs and issues sooner than our users do.  It is better for us to be frustrated with site issues that our end users.  All updates are reviewed by Discovery management and the current maintainers before deploying to production.

If issues are found, hotfix branches can be created from the **develop** branch and advance through the update process as normal.  This is one benefit to having a quick develop, test, production release cycle detached from timed sprints.

<br/>
