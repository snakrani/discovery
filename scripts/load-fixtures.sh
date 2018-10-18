#!/usr/bin/env bash
# Load data for the GSA PSHC discovery application, per the README instructions.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

# Load vendor related fixtures

./manage.py loaddata vendors/fixtures/locations.json
./manage.py loaddata vendors/fixtures/vendors.json # reqs: locations, setasides
./manage.py loaddata vendors/fixtures/poolmemberships.json # reqs: pool, vendor
./manage.py loaddata vendors/fixtures/samloads.json
./manage.py loaddata vendors/fixtures/contacts.json # reqs: vendors
./manage.py loaddata vendors/fixtures/contactemails.json # reqs: contacts
./manage.py loaddata vendors/fixtures/contactphones.json # reqs: contacts

# Load contract related fixtures

./manage.py loaddata contracts/fixtures/agencies.json
./manage.py loaddata contracts/fixtures/contractstatuses.json
./manage.py loaddata contracts/fixtures/pricingstructures.json
./manage.py loaddata contracts/fixtures/placesofperformance.json
./manage.py loaddata contracts/fixtures/contracts.json #reqs: naics, vendor, agency, contractstatus, pricingstructure, placeofperformance
./manage.py loaddata contracts/fixtures/fpdsloads.json #reqs: vendor
