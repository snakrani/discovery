

def get_category_fixtures():
    return [
        'keywords.json',
        'sin.json',
        'naics.json',
        'psc.json',
        'setasides.json', 
        'pools.json',
        'zones.json',
        'zonestates.json'
    ]


def get_vendor_fixtures():
    return get_category_fixtures() + [
        'locations.json', 
        'vendors.json',
        'managers.json',
        'managerphonenumbers.json',
        'manageremails.json',
        'contractmanagers.json',
        'projectmanagers.json', 
        'poolmemberships.json'        
    ]


def get_contract_fixtures():
    return get_vendor_fixtures() + [
        'contractstatuses.json',
        'pricingstructures.json',
        'placesofperformance.json', 
        'contracts.json'
    ]

    
def get_metadata_fixtures():
    return get_vendor_fixtures() + [
        'samloads.json',
        'fpdsloads.json'
    ]
