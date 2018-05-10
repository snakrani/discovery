#!/usr/bin/env bash
# Generate data for the GSA PSHC discovery application, per the README instructions.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

# Load category fixtures

./manage.py dump_categories

# Generate vendor related fixtures

./manage.py dumpdata vendors.location --indent=2 > vendors/fixtures/locations.json
./manage.py dumpdata vendors.vendor --indent=2 > vendors/fixtures/vendors.json # reqs: locations, managers, setasides
./manage.py dumpdata vendors.poolmembership --indent=2 > vendors/fixtures/poolmemberships.json # reqs: pool, vendor
./manage.py dumpdata vendors.manager --indent=2 > vendors/fixtures/managers.json
./manage.py dumpdata vendors.manageremail --indent=2 > vendors/fixtures/manageremails.json # reqs: managers
./manage.py dumpdata vendors.managerphonenumber --indent=2 > vendors/fixtures/managerphonenumbers.json # reqs: managers
./manage.py dumpdata vendors.contractmanager --indent=2 > vendors/fixtures/contractmanagers.json # reqs: managers
./manage.py dumpdata vendors.projectmanager --indent=2 > vendors/fixtures/projectmanagers.json # reqs: managers
./manage.py dumpdata vendors.samload --indent=2 > vendors/fixtures/samloads.json

# Generate contract related fixtures

./manage.py dumpdata contracts.placeofperformance --indent=2 > contracts/fixtures/placesofperformance.json
./manage.py dumpdata contracts.contract --indent=2 > contracts/fixtures/contracts.json #reqs: naics, vendor, piid
./manage.py dumpdata contracts.fpdsload --indent=2 > contracts/fixtures/fpdsloads.json #reqs: vendor
