#!/usr/bin/env bash
# Generate data for the GSA PSHC discovery application, per the README instructions.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

# Generate category fixtures

./manage.py dumpdata vendors.naics --indent=2 > vendors/fixtures/naics.json
./manage.py dumpdata vendors.setaside --indent=2 > vendors/fixtures/setasides.json
./manage.py dumpdata vendors.zone --indent=2 > vendors/fixtures/zones.json
./manage.py dumpdata vendors.zonestate --indent=2 > vendors/fixtures/zonestates.json # reqs: zones
./manage.py dumpdata vendors.pool --indent=2 > vendors/fixtures/pools.json # reqs: naics

# Generate vendor related fixtures

./manage.py dumpdata vendors.location --indent=2 > vendors/fixtures/locations.json
./manage.py dumpdata vendors.manager --indent=2 > vendors/fixtures/managers.json
./manage.py dumpdata vendors.managerphonenumber --indent=2 > vendors/fixtures/managerphonenumbers.json # reqs: managers
./manage.py dumpdata vendors.manageremail --indent=2 > vendors/fixtures/manageremails.json # reqs: managers
./manage.py dumpdata vendors.vendor --indent=2 > vendors/fixtures/vendors.json # reqs: locations, managers, setasides
./manage.py dumpdata vendors.poolpiid --indent=2 > vendors/fixtures/poolpiids.json # reqs: pool, vendor, zone
./manage.py dumpdata vendors.samload --indent=2 > vendors/fixtures/samloads.json

# Generate contract related fixtures

./manage.py dumpdata contract.placeofperformance --indent=2 > contract/fixtures/placesofperformance.json
./manage.py dumpdata contract.contract --indent=2 > contract/fixtures/contracts.json #reqs: naics, vendor, piid
./manage.py dumpdata contract.fpdsload --indent=2 > contract/fixtures/fpdsloads.json #reqs: vendor
