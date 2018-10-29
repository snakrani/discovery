

def get_category_fixtures():
    return [
        'keywords.json',
        'sin.json',
        'naics.json',
        'psc.json',
        'setasides.json',
        'tiers.json',
        'vehicles.json', 
        'pools.json',
        'states.json',
        'zones.json'
    ]


def get_vendor_fixtures():
    return get_category_fixtures() + [
        'locations.json', 
        'vendors.json',
        'contacts.json',
        'contactphones.json',
        'contactemails.json',
        'poolmemberships.json'        
    ]


def get_contract_fixtures():
    return get_vendor_fixtures() + [
        'agencies.json',
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
