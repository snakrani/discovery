

def get_category_fixtures():
    return [
        'naics.json', 
        'setasides.json', 
        'pools.json',
        'zones.json',
        'zonestates.json'
    ]


def get_vendor_fixtures():
    return get_category_fixtures() + [
        'locations.json', 
        'vendors.json', 
        'poolmembership.json'
    ]


def get_contract_fixtures():
    return get_vendor_fixtures() + [
        'placesofperformance.json', 
        'contracts.json'
    ]

    
def get_metadata_fixtures():
    return get_vendor_fixtures() + [
        'samloads.json',
        'fpdsloads.json'
    ]
