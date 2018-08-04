from django.test import tag

from test import cases as case

from acceptance.common import generate_schema
from acceptance.search import generate_search_tests


@tag('home')
class HomeTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = generate_schema({
        'includes': {
            'search': generate_search_tests()
        },
        'header': {
            'tags': ('title',),
            'wait': 'complete',
            'Discovery': 'title'
        },
        'vehicle_info_display': {
            'tags': ('info',),
            'h1.vehicle span': ('has_class', 'arrow-d'),
            'xpath://*[@id="discovery_vehicles"]/h1[1]': ('text__equal', 'One Acquisition Solution for Integrated Services (OASIS)'),
            'xpath://*[@id="discovery_vehicles"]/h1[1]/span': ('has_class', 'arrow-d'),
            'xpath://*[@id="discovery_vehicles"]/h1[2]': ('text__equal', 'Building Maintenance and Operations (BMO)'),
            'xpath://*[@id="discovery_vehicles"]/h1[2]/span': ('has_class', 'arrow-d'),
            'xpath://*[@id="discovery_vehicles"]/h1[3]': ('text__equal', 'Human Capital and Training Solutions (HCaTS)'),
            'xpath://*[@id="discovery_vehicles"]/h1[3]/span': ('has_class', 'arrow-d'),
            'xpath://*[@id="discovery_vehicles"]/h1[4]': ('text__equal', 'Professional Services Schedule (PSS)'),
            'xpath://*[@id="discovery_vehicles"]/h1[4]/span': ('has_class', 'arrow-d')
        },
        'sam_load_date': {
            'tags': ('info',),
            '#data_source_date_sam': ('text__matches', r'^[\d]*/[\d]*/[\d]*$')
        },
        'fpds_load_date': {
            'tags': ('info',),
            '#data_source_date_fpds': ('text__matches', r'^[\d]*/[\d]*/[\d]*$')
        },
        'footer': {
            'tags': ('info',),
            'link_text:OASIS Program Home': ('link__equal', 'http://www.gsa.gov/oasis'),
            'link_text:Check out our code on GitHub': ('link__equal', 'https://github.com/PSHCDevOps/discovery'),
            'span.cta_email_address': ('text__equal', 'pshc-dev@gsa.gov')
        } 
    })
