from test import cases as case


class HomeTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
        'header': {
            'Discovery': 'title'
        },
        'naics_filter': {
            'params': {
                'vehicle': 'OASIS_SB'
            },
            'naics-code': 'enabled'
        },
        'vehicle_filter': {
            'params': {
                'vehicle': 'OASIS_SB'
            },
            'vehicle-id': 'enabled'
        },
        'pool_filter': {
            'params': {
                'vehicle': 'OASIS_SB'
            },
            'pool-id': 'enabled'
        },
        'zone_filter': {
            'params': {
                'vehicle': 'OASIS_SB'
            },
            'zone-id': 'disabled'
        },
        'se_filter': {
            'params': {
                'vehicle': 'OASIS_SB'
            },
            'css:.se_filter': 'disabled'
        },
        'load_dates': {
            'wait': ('sec', 2),
            'data_source_date_sam': ('text__matches', r'^[\d]*/[\d]*/[\d]*$'),
            'data_source_date_fpds': ('text__matches', r'^[\d]*/[\d]*/[\d]*$')
        },
        'footer': {
            'link_text:OASIS Program Home': ('link__equal', 'http://www.gsa.gov/oasis'),
            'link_text:Check out our code on GitHub': ('link__equal', 'https://github.com/PSHCDevOps/discovery')
        } 
    }
