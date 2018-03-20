from test import cases as case


class BaseContractTest(case.ContractAPITestCase):
    def initialize(self):
        self.router = 'contracts'
        
    def validate_object(self, resp, base_key = []):
        resp.is_int(base_key + ['id'])
        resp.is_not_empty(base_key + ['piid'])
        resp.is_not_empty(base_key + ['agency_id'])
        resp.is_not_empty(base_key + ['agency_name'])
        resp.is_not_empty(base_key + ['date_signed'])
        resp.is_float(base_key + ['obligated_amount'])
        
        resp.is_not_empty(base_key + ['vendor', 'name'])
        resp.is_int(base_key + ['vendor', 'duns'])
        
        resp.is_float(base_key + ['annual_revenue'])
        resp.is_int(base_key + ['number_of_employees'])


class ContractListTest(BaseContractTest):  
    def schema(self):
        return {
            'ordering': (
                'id', 'piid', 
                'agency_id', 'agency_name', 
                'NAICS', 'PSC',
                'date_signed', 'completion_date', 'obligated_amount',
                'vendor__duns', 'vendor__cage', 'vendor__name',
                'point_of_contact', 'vendor_phone',
                'vendor_location__address', 
                'vendor_location__city', 
                'vendor_location__state', 
                'vendor_location__zipcode', 
                'vendor_location__congressional_district', 
                'status__name', 'pricing_type__name',
                'place_of_performance_location',
                'annual_revenue', 'number_of_employees'
            ),
            'pagination': {
                '@no_args': {},
                '@page': {'page': 3},
                '@count': {'count': 50},
                '@mixed': {'page': 2, 'count': 50}
            },
            'search': {
                '*search1': ('piid', 'iequal', 'NRC0807418'),
                '@search2': ('agency_name', 'imatches', 'NUCLEAR REGULATORY COMMISSION')
            },
            'fields': {
                'id': {
                    '*exact': 256,
                    '@lt': 500,
                    '@lte': 500, 
                    '@gt': 250, 
                    '@gte': 250,
                    '@range': (50, 100),
                    '@in': (2, 3, 5)
                },
                'piid': {
                    '*exact': 'NRC0804414_02',
                    '*iexact': 'nrc0804414_02',
                    '@in': ('NRC0804414_02', 'NRC3810699', 'SP470310D0002_0021'),
                    '@contains': 'D0002',
                    '@icontains': 'd0002',
                    '@startswith': 'FA',
                    '@istartswith': 'fa',
                    '@endswith': '_0002',
                    '@iendswith': 'a16p',
                    '@regex': '\d+_\d+',
                    '@iregex': '[a-z]{2}g15'
                },
                'agency_id': {
                    '@exact': '8000',
                    '@iexact': '8000',
                    '@in': ('8000', '6800', '2050')
                },
                'agency_name': {
                    '@exact': 'INTERNAL REVENUE SERVICE',
                    '@iexact': 'Internal Revenue Service',
                    '@in': ('INTERNAL REVENUE SERVICE', 'CONSUMER FINANCIAL PROTECTION BUREAU', 'FEDERAL ACQUISITION SERVICE'),
                    '@contains': 'ACQUISITION',
                    '@icontains': 'acquisition',
                    '@startswith': 'DEPT',
                    '@istartswith': 'dept',
                    '@endswith': 'GUARD',
                    '@iendswith': 'guard',
                    '@regex': '^[A-Z]{4}',
                    '@iregex': 'office\s+'
                },
                'NAICS': {
                    '@exact': '541330',
                    '@iexact': '541712',
                    '@in': ("541711", "238290", "561730"),
                    '@contains': '622',
                    '@icontains': '622',
                    '@startswith': '54',
                    '@istartswith': '2382',
                    '@endswith': '711',
                    '@iendswith': '711',
                    '@regex': '^\d+622',
                    '@iregex': '^(23|56)'
                },
                'PSC': {
                    '@exact': 'U099',
                    '@iexact': 'ad26',
                    '@in': ("U099", "AD260", "R425"),
                    '@contains': '707',
                    '@icontains': 'ad',
                    '@startswith': 'R',
                    '@istartswith': 'r',
                    '@endswith': '2',
                    '@iendswith': 'z',
                    '@regex': '[^\d]+$',
                    '@iregex': '^(u0|ad)'
                },
                'date_signed': {
                    '@date': '2007-07-09',
                    '@year': '2007',
                    '@month': '7',
                    '@day': '9',
                    '@week': '5',
                    '@week_day': '2',
                    '@quarter': '2'
                },
                'completion_date': {
                    '@date': '2012-05-10',
                    '@year': '2012',
                    '@month': '5',
                    '@day': '10',
                    '@week': '23',
                    '@week_day': '4',
                    '@quarter': '3'
                },
                'obligated_amount': {
                    '@exact': 150000,
                    '@lt': 0,
                    '@lte': 10000, 
                    '@gt': 100000, 
                    '@gte': 200000,
                    '@range': (50000, 500000),
                    '@in': (-80000, 40640, 10250)
                },
                'point_of_contact': {
                    '@exact': 'PADDS.W31P4Q@KO.ARMY.MIL',
                    '@iexact': 'padds.w31P4Q@KO.army.mil',
                    '@in': ("PADDS.W31P4Q@KO.ARMY.MIL", "USERCW@SA5700.FA8604", "MARASHULTZ@GSA.GOV"),
                    '@contains': 'GSA',
                    '@icontains': 'gsa',
                    '@startswith': 'USER',
                    '@istartswith': 'user',
                    '@endswith': 'FA8602',
                    '@iendswith': 'mil',
                    '@regex': '\d+$',
                    '@iregex': '\.[a-z]+\d+$'
                },
                'vendor_phone': {
                    '@exact': '918-583-9900',
                    '@iexact': '918-583-9900',
                    '@in': ("918-583-9900", "301-948-4232", "619-298-0888"),
                    '@contains': '-948-',
                    '@icontains': '-948-',
                    '@startswith': '505',
                    '@istartswith': '703',
                    '@endswith': '7637',
                    '@iendswith': '6767',
                    '@regex': '^\d{3}-255-\d{4}$',
                    '@iregex': '(571|202)-\d{3}'
                },
                'annual_revenue': {
                    '@exact': 1200000,
                    '@lt': 500000,
                    '@lte': 300000, 
                    '@gt': 4000000, 
                    '@gte': 5500000,
                    '@range': (100000, 3000000),
                    '@in': (250000, 27019000, 15000000)
                },
                'number_of_employees': {
                    '@exact': 210,
                    '@lt': 190,
                    '@lte': 200, 
                    '@gt': 100, 
                    '@gte': 500,
                    '@range': (300, 1000),
                    '@in': (580, 70, 900)
                },
                'status__code': {
                    '@exact': 'C1',
                    '@iexact': 'c1',
                    '@in': ('A', 'C2', 'X', 'F')
                },
                'status__name': {
                    '@exact': 'Completed',
                    '@iexact': 'currEnt',
                    '@in': ("Current", "Completed", "Close out"),
                    '@contains': 'Terminated',
                    '@icontains': 'terminated',
                    '@startswith': 'C',
                    '@istartswith': 'c',
                    '@endswith': 'Cause',
                    '@iendswith': 'cause',
                    '@regex': '(Current|Completed)',
                    '@iregex': '(current|completed)'
                },
                'pricing_type__code': {
                    '@exact': 'Y',
                    '@iexact': 'u',
                    '@in': ('M', '3', 'K', 'Z')
                },
                'pricing_type__name': {
                    '@exact': 'Firm Fixed Price',
                    '@iexact': 'firm fixed price',
                    '@in': ("Firm Fixed Price", "Time and Materials"),
                    '@contains': 'Price',
                    '@icontains': 'price',
                    '@startswith': 'Cost',
                    '@istartswith': 'cost',
                    '@endswith': 'Fee',
                    '@iendswith': 'fee',
                    '@regex': '^Fixed\s+',
                    '@iregex': '^fixed\s+'
                },
                'place_of_performance__country_code': {
                    '@exact': 'USA',
                    '@iexact': 'usa',
                    '@in': ("USA","JPN","MDA","GBR")
                },
                'place_of_performance__country_name': {
                    '@exact': 'United States',
                    '@iexact': 'united states',
                    '@in': ("United States","United Kingdom"),
                    '@contains': 'United',
                    '@icontains': 'united',
                    '@startswith': 'Ant',
                    '@istartswith': 'ant',
                    '@endswith': 'non',
                    '@iendswith': 'NON',
                    '@regex': '^United (States|Kingdom)$',
                    '@iregex': '^united (states|kingdom)$'
                },
                'place_of_performance__state': {
                    '@exact': 'DC',
                    '@iexact': 'dc',
                    '@in': ("DC","CA","TX","VA")
                },
                'place_of_performance__zipcode': {
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
                'vendor_location__address': {
                    '@exact': '7000 Muirkirk Meadows Dr',
                    '@iexact': '7000 muirkirk meadows dr',
                    '@in': ("1002 Explorer Blvd", "8600 Boeing Dr"),
                    '@contains': 'Northbrook',
                    '@icontains': 'dEErfield pOnd',
                    '@startswith': '7500',
                    '@istartswith': '360a',
                    '@endswith': 'Ave',
                    '@iendswith': 'ave',
                    '@regex': 'Ste \d+$',
                    '@iregex': 'ste \d+$'
                },
                'vendor_location__city': {
                    '@exact': 'Lexington',
                    '@iexact': 'vienna',
                    '@in': ("Lanham", "Frederick", "Huntsville"),
                    '@contains': 'vill',
                    '@icontains': 'of',
                    '@startswith': 'Mc',
                    '@istartswith': 'mc',
                    '@endswith': 'polis',
                    '@iendswith': 'POLIS',
                    '@regex': 'City',
                    '@iregex': 'TOWN'
                },
                'vendor_location__state': {
                    '@exact': 'DC',
                    '@iexact': 'dc',
                    '@in': ("DC","CA","TX","VA")
                },
                'vendor_location__zipcode': {
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
                'vendor_location__congressional_district': {
                    '@exact': '07',
                    '@iexact': '07',
                    '@in': ("07", "04", "08", "01")
                },      
                'vendor__name': {
                    '@exact': 'Zero Waste Solutions',
                    '@iexact': 'urs federal services, inc.',
                    '@in': ('Suntiva', 'Trademasters', 'PowerTrain'),
                    '@contains': 'Research',
                    '@icontains': 'technologies',
                    '@startswith': 'M',
                    '@istartswith': 'global',
                    '@endswith': 'LLC',
                    '@iendswith': 'llc',
                    '@regex': '\d+',
                    '@iregex': 'inc\.?$'
                },
                'vendor__duns': {
                    '@lt': '193460839',
                    '@lte': '193460839', 
                    '@gt': '193460839', 
                    '@gte': '193460839',
                    '@range': '074108176,196004394',
                    '@in': ('114896066', '555498187', '790984186')
                },
                'vendor__cage': {
                    '@exact': '4WPK2',
                    '@iexact': '4WPK2',
                    '@in': ('1RUU6', '4ZSH3', '4YAG9')
                },
                'vendor__sam_status': {
                    '@exact': 'ACTIVE',
                    '@iexact': 'active',
                    '@in': "ACTIVE"
                },
                'vendor__sam_activation_date': {
                    '@date': '2018-02-09',
                    '@year': '2018',
                    '@month': '2',
                    '@day': '9',
                    '@week': '5',
                    '@week_day': '2',
                    '@quarter': '1'
                },
                'vendor__sam_expiration_date': {
                    '@date': '2019-02-09',
                    '@year': '2019',
                    '@month': '2',
                    '@day': '9',
                    '@week': '5',
                    '@week_day': '3',
                    '@quarter': '1'
                },
                'vendor__sam_exclusion': {
                    '-exact': True,
                    '@exact': False,
                },
                'vendor__sam_url': {
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
                'vendor__sam_location__address': {
                    '@exact': '7000 Muirkirk Meadows Dr',
                    '@iexact': '7000 muirkirk meadows dr',
                    '@in': ("1002 Explorer Blvd", "8600 Boeing Dr"),
                    '@contains': 'Northbrook',
                    '@icontains': 'dEErfield pOnd',
                    '@startswith': '7500',
                    '@istartswith': '360a',
                    '@endswith': 'Ave',
                    '@iendswith': 'ave',
                    '@regex': 'Ste \d+$',
                    '@iregex': 'ste \d+$'
                },
                'vendor__sam_location__city': {
                    '@exact': 'Lexington',
                    '@iexact': 'vienna',
                    '@in': ("Lanham", "Frederick", "Huntsville"),
                    '@contains': 'vill',
                    '@icontains': 'of',
                    '@startswith': 'Mc',
                    '@istartswith': 'mc',
                    '@endswith': 'polis',
                    '@iendswith': 'POLIS',
                    '@regex': 'City',
                    '@iregex': 'TOWN'
                },
                'vendor__sam_location__state': {
                    '@exact': 'DC',
                    '@iexact': 'dc',
                    '@in': ("DC","CA","TX","VA")
                },
                'vendor__sam_location__zipcode': {
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
                'vendor__sam_location__congressional_district': {
                    '@exact': '07',
                    '@iexact': '07',
                    '@in': ("07", "04", "08", "01")
                },
                'vendor__pools__piid': {
                    '@exact': 'GS00Q14OADS121',
                    '@iexact': 'gs00q14Oads121',
                    '@in': ("GS00Q14OADS121", "GS00Q14OADS608"),
                    '@contains': 'OAD',
                    '@icontains': 'Oad',
                    '@startswith': 'GS02',
                    '@istartswith': 'gs02',
                    '@endswith': '102',
                    '@iendswith': 's102',
                    '@regex': '^GS\d+',
                    '@iregex': '^(gs06|gs00)'
                },
                'vendor__pools__pool__id': {
                    '@exact': 'BMO_SB_10',
                    '@iexact': 'hcaTs_Sb_2',
                    '@in': ("BMO_8", "OASIS_4", "HCATS_SB_1")
                },
                'vendor__pools__pool__name': {
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
                'vendor__pools__pool__number': {
                    '@exact': '8',
                    '@iexact': '9',
                    '@in': ('1', '3', '5B', '16')
                },
                'vendor__pools__pool__vehicle': {
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
                'vendor__pools__pool__threshold': {
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
                'vendor__pools__pool__naics__code': {
                    '@exact': '541330',
                    '@iexact': '541712c',
                    '@in': ("541711", "238290", "561730B"),
                    '@contains': '622',
                    '@icontains': 'b',
                    '@startswith': '54',
                    '@istartswith': '2382',
                    '@endswith': 'A',
                    '@iendswith': 'c',
                    '@regex': '[^\d]+$',
                    '@iregex': '^(23|56)'
                },
                'vendor__pools__pool__naics__root_code': {
                    '@exact': '541330',
                    '@iexact': '541712',
                    '@in': ("541711", "238290", "561730"),
                    '@contains': '622',
                    '@icontains': '990',
                    '@startswith': '61',
                    '@istartswith': '5617',
                    '@endswith': '10',
                    '@iendswith': '20',
                    '@regex': '^[\d]+$',
                    '@iregex': '^(23|56)'
                },
                'vendor__pools__pool__naics__description': {
                    '@exact': 'Outdoor Advertising',
                    '@iexact': 'hvac maintenance',
                    '@in': ("Payroll Services", "Commissioning Services", "Testing Laboratories"),
                    '@contains': 'Accounting',
                    '@icontains': 'rEPair',
                    '@startswith': 'Engineering',
                    '@istartswith': 'r',
                    '@endswith': 'Services',
                    '@iendswith': 'advertIsing',
                    '@regex': '[/]+',
                    '@iregex': 'water\s+based'
                },
                'vendor__pools__setasides__code': {
                    '@exact': 'QF',
                    '@iexact': 'a2',
                    '@in': ('XX', 'A5', '27')
                },
                'vendor__pools__setasides__name': {
                    '@exact': 'WO',
                    '@iexact': 'hubz',
                    '@in': ('8(A)', 'SDVO', 'HubZ')
                },
                'vendor__pools__setasides__description': {
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
                'vendor__pools__setasides__far_order': {
                    '@exact': 3,
                    '@lt': 4,
                    '@lte': 4, 
                    '@gt': 3, 
                    '@gte': 3,
                    '@range': (2, 5),
                    '@in': (2, 3, 5)
                },
                'vendor__pools__zones__id': {
                    '@exact': 2,
                    '@lt': 4,
                    '@lte': 4, 
                    '@gt': 3, 
                    '@gte': 3,
                    '@range': (2, 5),
                    '@in': (2, 3, 5)
                },
                'vendor__pools__zones__state': {
                    '@exact': 'PA',
                    '@iexact': 'mE',
                    '@in': ('PA', 'NC', 'TX', 'NY')
                },
                'vendor__pools__cms__name': {
                    '@exact': 'Ken Scott',
                    '@iexact': 'daniel eke',
                    '@in': ("Ken Scott", "Daniel Eke"),
                    '@contains': 'Taylor',
                    '@icontains': 'taylor',
                    '@startswith': 'Ben',
                    '@istartswith': 'ben',
                    '@endswith': 'Shea',
                    '@iendswith': 'shea',
                    '@regex': '^[A-Za-z]{4}\s+',
                    '@iregex': '^da(n|na)'
                },
                'vendor__pools__cms__phone': {
                    '@exact': '703-821-0678',
                    '@iexact': '703-821-0678',
                    '@in': ("703-821-0678", "571-262-3144", "937-912-6102"),
                    '@contains': '-426-',
                    '@icontains': '-426-',
                    '@startswith': '757',
                    '@istartswith': '757',
                    '@endswith': '6551',
                    '@iendswith': '6551',
                    '@regex': 'x\d+$',
                    '@iregex': '(304|703)-\d{3}'
                },
                'vendor__pools__cms__email': {
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
                },
                'vendor__pools__pms__name': {
                    '@exact': 'Phil Sahady',
                    '@iexact': 'phil sahady',
                    '@in': ("Phil Sahady", "Charles A. Colon,  III"),
                    '@contains': 'Glass',
                    '@icontains': 'glass',
                    '@startswith': 'John',
                    '@istartswith': 'john',
                    '@endswith': 'Carroll',
                    '@iendswith': 'carroll',
                    '@regex': '^[A-Za-z]{4}\s+',
                    '@iregex': '^dr\.?'
                },
                'vendor__pools__pms__phone': {
                    '@exact': '703-642-2380',
                    '@iexact': '703-642-2380',
                    '@in': ("703-642-2380", "937-912-6102", "703-435-2260"),
                    '@contains': '-824-',
                    '@icontains': '-824-',
                    '@startswith': '719',
                    '@istartswith': '719',
                    '@endswith': '6102',
                    '@iendswith': '6102',
                    '@regex': 'x\d+$',
                    '@iregex': '(937|703)-\d{3}'
                },
                'vendor__pools__pms__email': {
                    '@exact': 'OASIS@niksoft.com',
                    '@iexact': 'oasis@niksoft.com',
                    '@in': ("OASIS@niksoft.com", "OASISSB@integrity-apps.com", "hcats@arcaspicio.com"),
                    '@contains': 'apps',
                    '@icontains': 'APPS',
                    '@startswith': 'hcats',
                    '@istartswith': 'HcAtS',
                    '@endswith': 'com',
                    '@iendswith': 'cOM',
                    '@regex': '\d+',
                    '@iregex': '\.(com|net)$'
                }                
            }
        }


class ContractRetrieveTest(BaseContractTest):
    def schema(self):
        return {
            'object': {
                '&1': ('piid', 'equal', 'DAAE0799CL001'),
                '&162': ('piid', 'equal', 'SP470310D0002_0044'),
                '&828': ('name', 'equal', 'USZA2202D0015_0194'),
                '#345C': (),
                '#ABCDEFG': ()
            }
        }
