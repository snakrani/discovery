from test import cases as case


class HomeTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
        'title': 'Discovery',
        'vehicle_naics_filter': {
            'params': {
                'vehicle': 'oasis_sb'
            },
            'naics-code': 'enabled',
            'placeholder': 'enabled',
            'css:.se_filter': 'disabled'
        },
        'footer': {
            'link_text:OASIS Program Home': ('link', 'http://www.gsa.gov/oasis'),
            'link_text:Check out our code on GitHub': ('link', 'https://github.com/PSHCDevOps/discovery')
        } 
    }
