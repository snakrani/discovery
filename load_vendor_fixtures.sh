#!/usr/bin/env bash
# Load data for the 18F/discovery application, per the README instructions.

# Load pre-existing fixtures in the prescribed order.

./manage.py loaddata vendors/fixtures/naics.json
./manage.py loaddata vendors/fixtures/pools.json
./manage.py loaddata vendors/fixtures/setasides.json

# Load the new vendors fixture.

./manage.py loaddata api/fixtures/vendors.json
