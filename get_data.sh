#!/usr/bin/env bash
# Load data for the 18F/discovery application, per the README instructions.

# Generate a vendors fixture from the OASIS data.

./generate_vendors_fixture.py

# Load pre-existing fixtures in the prescribed order.

./manage.py loaddata vendor/fixtures/naics.json
./manage.py loaddata vendor/fixtures/pools.json
./manage.py loaddata vendor/fixtures/setasides.json

# Load the new vendors fixture.

./manage.py loaddata vendor/fixtures/vendors.json

# Load vendors.

./manage.py load_vendors

# Load contract history.

./manage.py load_fpds