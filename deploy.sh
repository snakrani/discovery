#!/bin/bash

#To Deploy
# Create a personal access token at https://github.com/settings/applications
# put that token in a GH_KEY env variable
# then run ./deploy.sh GIT_REF ENVIRONMENT
# so ./deploy.sh master demo or ./deploy.sh master production

curl  -H "Accept: application/vnd.github.cannonball-preview+json" \
      -H "Authorization: token $GH_KEY" \
      -X POST --data "{ \"ref\":\"$1\", \"task\":\"deploy\", \"auto_merge\": false, \"required_contexts\": [], \"environment\" : \"$2\" }" \
      https://api.github.com/repos/18F/mirage/deployments
