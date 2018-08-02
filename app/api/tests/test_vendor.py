from test import cases as case
from test import fixtures as data


class VendorTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_vendor_fixtures()
    schema = {
            'object': {
                '&007901598': ('name', 'exact', 'BATTELLE MEMORIAL INSTITUTE'),
                '&133239397': ('name', 'exact', 'MIRACLE SYSTEMS, LLC'),
                '&001014182': ('name', 'exact', 'DYNAMICS RESEARCH CORPORATION'),
                '#345': (),
                '#ABCDEFG': ()
            },
            'ordering': (
                'name', 'duns', 'cage', 
                'sam_status', 'sam_exclusion', 'sam_url',
                'sam_location__address', 
                'sam_location__city', 
                'sam_location__state', 
                'sam_location__zipcode', 
                'sam_location__congressional_district', 
                'sam_location_citystate',
                'annual_revenue', 
                'number_of_employees', 
                'number_of_contracts'
            ),
            'pagination': {
                '@no_args': {},
                '@page': {'page': 3},
                '@count': {'count': 10},
                '@mixed': {'page': 2, 'count': 10}
            },
            'search': {
                '@search1': ('name', 'regex', 'SERVICES'),
                '*search2': ('duns', 'exact', '830333824'),
                '*search3': ('cage', 'exact', '3K773')
            },
            'fields': {
                'name': {
                    '*exact': 'DYNAMICS RESEARCH CORPORATION',
                    '@iexact': 'native energy & technology, inc.',
                    '@in': ('ENGILITY CORPORATION', 'CBRE', 'POWERTRAIN'),
                    '@contains': 'RESEARCH',
                    '@icontains': 'technologies',
                    '@startswith': 'M',
                    '@istartswith': 'applied',
                    '@endswith': 'LLC',
                    '@iendswith': 'llc',
                    '@regex': '\d+',
                    '@iregex': 'inc\.?$'
                },
                'duns': {
                    '*exact': '097967608',
                    '@lt': '193460839',
                    '@lte': '193460839', 
                    '@gt': '193460839', 
                    '@gte': '193460839',
                    '@range': '074108176,196004394',
                    '@in': ('055124077', '838295400', '003184462')
                },
                'cage': {
                    '*exact': '3A3Q8',
                    '*iexact': '3A3Q8',
                    '@in': ('4L767', '4SJK4', '4U825')
                },
                'sam_status': {
                    '@exact': 'ACTIVE',
                    '@iexact': 'active',
                    '@in': "ACTIVE"
                },
                'sam_activation_date': {
                    '@date': '2018-02-09',
                    '@year': '2018',
                    '@month': '2',
                    '@day': '9',
                    '@week': '5',
                    '@week_day': '2',
                    '@quarter': '1'
                },
                'sam_expiration_date': {
                    '@date': '2019-02-09',
                    '@year': '2019',
                    '@month': '2',
                    '@day': '9',
                    '@week': '5',
                    '@week_day': '3',
                    '@quarter': '1'
                },
                'sam_exclusion': {
                    '-exact': True,
                    '@exact': False,
                },
                'sam_url': {
                    '@exact': 'http://www.act-corp.com',
                    '@iexact': 'http://WWW.ACT-CORP.COM',
                    '@in': ("http://www.sainc.com", "https://www.atlasresearch.us"),
                    '@contains': 'sys',
                    '@icontains': 'SYS',
                    '@startswith': 'http://www.',
                    '@istartswith': 'HTTP://WWW.',
                    '@endswith': '.com',
                    '@iendswith': '.COM',
                    '@regex': '\d+',
                    '@iregex': 'www\.[^\.]+\.com'
                },
                'sam_location__address': {
                    '@exact': '7000 Muirkirk Meadows Dr',
                    '@iexact': '7000 muirkirk meadows dr',
                    '@in': ("1002 Explorer Blvd", "8600 Boeing Dr"),
                    '@contains': 'South',
                    '@icontains': 'dEErfield pOnd',
                    '@startswith': '7500',
                    '@istartswith': '6710 ro',
                    '@endswith': 'Ave',
                    '@iendswith': 'ave',
                    '@regex': 'Ste \d+$',
                    '@iregex': 'ste \d+$'
                },
                'sam_location__city': {
                    '@exact': 'Carlisle',
                    '@iexact': 'arlington',
                    '@in': ("Atlanta", "Reston", "Northville"),
                    '@contains': 'vill',
                    '@icontains': 'on',
                    '@startswith': 'Mc',
                    '@istartswith': 'mc',
                    '@endswith': 'ville',
                    '@iendswith': 'DA',
                    '@regex': 'Springs',
                    '@iregex': 'TOWN'
                },
                'sam_location__state': {
                    '@exact': 'DC',
                    '@iexact': 'dc',
                    '@in': ("DC","CA","TX","VA")
                },
                'sam_location__zipcode': {
                    '@exact': '20190',
                    '@iexact': '20190',
                    '@in': ("20190", "93033", "22102"),
                    '@contains': '210',
                    '@icontains': '210',
                    '@startswith': '35',
                    '@istartswith': '35',
                    '@endswith': '710',
                    '@iendswith': '710',
                    '@regex': '^[13579]+',
                    '@iregex': '^[13579]+'
                },
                'sam_location__congressional_district': {
                    '@exact': '07',
                    '@iexact': '07',
                    '@in': ("07", "04", "08", "01")
                },
                'pools__pool__id': {
                    '@exact': 'BMO_SB_10',
                    '@iexact': 'hcaTs_Sb_2',
                    '@in': ("BMO_8", "OASIS_4", "HCATS_SB_1")
                },
                'pools__piid': {
                    '@exact': 'GS00Q14OADU208',
                    '@iexact': 'gs00Q14Oadu208',
                    '@in': ("GS00Q14OADU343", "GS02Q16DCR0086"),
                    '@contains': 'OAD',
                    '@icontains': 'Oad',
                    '@startswith': 'GS02',
                    '@istartswith': 'gs02',
                    '@endswith': '102',
                    '@iendswith': 's102',
                    '@regex': '^GS\d+',
                    '@iregex': '^(gs06|gs00)'
                },
                'pools__expiration_8a_date': {
                    '@date': '2022-07-19',
                    '@year': '2017',
                    '@month': '7',
                    '@day': '19',
                    '@week': '32',
                    '@week_day': '3',
                    '@quarter': '1'
                },
                'pools__pool__name': {
                    '@exact': 'Elevator Maintenance',
                    '@iexact': 'janitoRial',
                    '@in': ("Roofing Services", "Plumbing and Pipefitting"),
                    '@contains': 'Waste',
                    '@icontains': 'energy engineering',
                    '@startswith': 'HVAC',
                    '@istartswith': 'hvac',
                    '@endswith': 'Maintenance',
                    '@iendswith': 'dEVelopment',
                    '@regex': '\d+$',
                    '@iregex': 'air.*development$'
                },
                'pools__pool__number': {
                    '@exact': '8',
                    '@iexact': '9',
                    '@in': ('1', '3', '5B', '16')
                },
                'pools__pool__vehicle': {
                    '@exact': 'OASIS_SB',
                    '@iexact': 'oasis',
                    '@in': ("HCATS", "BMO_SB"),
                    '@contains': 'SB',
                    '@icontains': 'oasis',
                    '@startswith': 'O',
                    '@istartswith': 'bm',
                    '@endswith': 'SB',
                    '@iendswith': '_sb',
                    '@regex': '^(OASIS|HCATS)_SB$',
                    '@iregex': '^(oaSis|hCaTs)_Sb$'
                },
                'pools__pool__threshold': {
                    '@exact': '$15 million',
                    '@iexact': '$7.5 MILLION',
                    '@in': ("1000 employee", "$18 million", "500 employee"),
                    '@contains': 'employee',
                    '@icontains': 'EmplOYeE',
                    '@startswith': '$38.5',
                    '@istartswith': '$38.5',
                    '@endswith': 'million',
                    '@iendswith': 'MillIon',
                    '@regex': '^\d+\s+',
                    '@iregex': '(500 EMPLOYEE|MILLION)'
                },
                'pools__pool__naics__code': {
                    '@exact': '541330',
                    '@iexact': '561710',
                    '@in': ("541711", "238290", "561730"),
                    '@contains': '622',
                    '@icontains': '622',
                    '@startswith': '54',
                    '@istartswith': '2382',
                    '@endswith': '30',
                    '@iendswith': '30',
                    '@regex': '^54\d+0$',
                    '@iregex': '^(23|56)'
                },
                'pools__pool__naics__description': {
                    '@exact': 'Outdoor Advertising',
                    '@iexact': 'meDIA representatives',
                    '@in': ("Payroll Services", "Commissioning Services", "Testing Laboratories"),
                    '@contains': 'Accounting',
                    '@icontains': 'heating',
                    '@startswith': 'Engineering',
                    '@istartswith': 'r',
                    '@endswith': 'Services',
                    '@iendswith': 'advertIsing',
                    '@regex': 'Services$',
                    '@iregex': 'apprentice(ship)?'
                },
                'pools__pool__naics__sin__code': {
                    '@exact': '100-03',
                    '@iexact': 'c871-202',
                    '@in': ("100-03", "520-14", "541-4G", "51-B36-2A"),
                    '@contains': '4B',
                    '@icontains': '-4b',
                    '@startswith': '51',
                    '@istartswith': 'c132',
                    '@endswith': '03',
                    '@iendswith': '2a',
                    '@regex': '[A-Z]\d+\-\d+$',
                    '@iregex': '^(C87|51)'
                },
                'pools__pool__naics__keywords__name': {
                    '@exact': 'Cooking Equipment',
                    '@iexact': 'ancillary supplies and / or services',
                    '@in': ("Elemental Analyzers", "Energy Consulting Services", "Environmental Consulting Services"),
                    '@contains': 'Support',
                    '@icontains': 'support',
                    '@startswith': 'Marine',
                    '@istartswith': 'edu',
                    '@endswith': 'Services',
                    '@iendswith': 'services',
                    '@regex': '(Training|Consulting)',
                    '@iregex': '^(vocational|strategic)'
                },
                'pools__setasides__code': {
                    '@exact': 'QF',
                    '@iexact': 'a2',
                    '@in': ('XX', 'A5', '27')
                },
                'pools__setasides__name': {
                    '@exact': 'WO',
                    '@iexact': 'hubz',
                    '@in': ('8(A)', 'SDVO', 'HubZ')
                },
                'pools__setasides__description': {
                    '@exact': 'Veteran Owned',
                    '@iexact': 'hubzone',
                    '@in': ("8(A)", "Woman Owned", "Small Disadvantaged Business"),
                    '@contains': 'Disadvantaged',
                    '@icontains': 'woman',
                    '@startswith': '8',
                    '@istartswith': 'hu',
                    '@endswith': 'Owned',
                    '@iendswith': 'owned',
                    '@regex': '^\d+',
                    '@iregex': 'Vet(eran)?'
                },
                'pools__setasides__far_order': {
                    '@exact': 3,
                    '@lt': 4,
                    '@lte': 4, 
                    '@gt': 3, 
                    '@gte': 3,
                    '@range': (2, 5),
                    '@in': (2, 3, 5)
                },
                'pools__zones__id': {
                    '@exact': 2,
                    '@lt': 4,
                    '@lte': 4, 
                    '@gt': 3, 
                    '@gte': 3,
                    '@range': (2, 5),
                    '@in': (2, 3, 5)
                },
                'pools__zones__states__code': {
                    '@exact': 'PA',
                    '@iexact': 'mE',
                    '@in': ('PA', 'NC', 'TX', 'NY')
                },
                'pools__contacts__name': {
                    '@exact': 'Ken Scott',
                    '@iexact': 'daniel eke',
                    '@in': ("Ken Scott", "Daniel Eke"),
                    '@contains': 'Taylor',
                    '@icontains': 'taylor',
                    '@startswith': 'Ben',
                    '@istartswith': 'ben',
                    '@endswith': 'Scott',
                    '@iendswith': 'scott',
                    '@regex': '^[A-Za-z]{4}\s+',
                    '@iregex': '^da(n|na)'
                },
                'pools__contacts__phones__number': {
                    '@exact': '703-821-0678',
                    '@iexact': '703-821-0678',
                    '@in': ("703-821-0678", "571-262-3144", "937-912-6102"),
                    '@contains': '-882-',
                    '@icontains': '-882-',
                    '@startswith': '757',
                    '@istartswith': '757',
                    '@endswith': '6551',
                    '@iendswith': '6551',
                    '@regex': 'x\s*\d+$',
                    '@iregex': '(304|703)-\d{3}'
                },
                'pools__contacts__emails__address': {
                    '@exact': 'OASIS@act-i.com',
                    '@iexact': 'oasis@act-i.com',
                    '@in': ("OASIS@act-i.com", "hcats_sb@deepmile.com", "Finance@exemplarent.com"),
                    '@contains': 'ibm',
                    '@icontains': 'IbM',
                    '@startswith': 'hcats',
                    '@istartswith': 'HcAtS',
                    '@endswith': 'com',
                    '@iendswith': 'cOM',
                    '@regex': '\d+',
                    '@iregex': '\.(com|net)$'
                }
            }
        }


    def initialize(self):
        self.router = 'vendors'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['name'])
        resp.is_int(base_key + ['duns'])
        resp.is_int(base_key + ['duns_4'])
                
        if resp.check('is_not_in', base_key + ['duns'], ('614155380', '148815173', '831340356', '246802545')):
            resp.is_not_empty(base_key + ['cage'])
            resp.is_not_empty(base_key + ['sam_status'])
            resp.is_not_none(base_key + ['sam_exclusion'])
            resp.is_not_empty(base_key + ['sam_activation_date'])
            resp.is_not_empty(base_key + ['sam_expiration_date'])
