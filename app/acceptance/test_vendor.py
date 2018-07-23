from test import cases as case

from acceptance.common import generate_schema


class VendorTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
  
    schema = generate_schema({
        'actions': {
            'unfiltered': {
                'params': {'args': '102067378', 'test': 'true'},
                'naics': ('all', 2),
                'membership_filters': (None, 4, 0, 0, {
                    1: ('Mary C. Dickens', '256-964-5213', 'cdickens@colsa.com')
                }, {
                    1: ('VO', 'SDVO')
                }),
                'vendor_sam': ('5/18/19',),
                'vendor_info': ('COLSA CORPORATION', '102067378', '4U825', '965', '$197,000,000'),
                'vendor_address': ('6728 Odyssey Dr', 'Huntsville, AL 35806', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/102067378/csv/?',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics': {
                'params': {'args': '139727148', 'test': 'true', 'naics': '541214'},
                'action': ('#naics-code', 'select[541214]'),
                'naics': ('541214', 31),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Tania Koles', '571-414-4033', 'OASIS@accenturefederal.com')
                }),
                'vendor_sam': ('4/5/19',),
                'vendor_info': ('ACCENTURE FEDERAL SERVICES LLC', '139727148', '1ZD18', '380', '$65,000,000'),
                'vendor_address': ('800 North Glebe Rd #300', 'Arlington, VA 22203', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/139727148/csv/?naics=541214',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'membership': {
                'params': {'args': '038523239', 'test': 'true', 'memberships': 'GS10F0175M'},
                'action': ('#GS10F0175M', 'click'),
                'naics': ('all', 7),
                'membership_filters': ('GS10F0175M', 1, 1, 0, {
                    1: ('', '907-455-6777', 'tdelong@abrinc.com')
                }),
                'vendor_sam': ('11/20/18',),
                'vendor_info': ('ABR INC', '038523239', '0Y330', '49', '$13,967,623'),
                'vendor_address': ('2842 Goldstream Rd', 'Fairbanks, AK 99709', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/139727148/csv/?memberships=GS10F0175M',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'mixed': {
                'params': {'args': '114214211', 'test': 'true', 'memberships': 'GS10F0081V', 'naics': '541611'},
                'action': (('#naics-code', 'select[541611]'), ('#GS10F0081V', 'click')),
                'naics': ('541611', 16),
                'membership_filters': ('GS10F0081V', 1, 1, 0, {
                    1: ('', '703-840-3491', 'doc.grantham@6Ksystems.com')
                }),
                'vendor_sam': ('6/28/19',),
                'vendor_info': ('6K SYSTEMS, INC.', '114214211', '1ZJK7', '100', '$5,666,666'),
                'vendor_address': ('11710 Plaza America Dr Ste 810', 'Reston, VA 20190', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/114214211/csv/?naics=541611&memberships=GS10F0081V',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'sorting': {
                'params': {'args': '129304551', 'test': 'true', 'ordering': '-obligated_amount'},
                'action': ('th.h_value', 'click'),
                'naics': ('all', 15),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Donald Hill III', '202-434-8470', 'dhill@actionfacilities.com')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('ACTION FACILITIES MANAGEMENT, INC.', '129304551', '3EET9', '182', '$14,600,000'),
                'vendor_address': ('115 Malone Dr', 'Morgantown, WV 26501', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/129304551/csv/?ordering=-obligated_amount',),
                'contract_table': (5, 'h_value', 'desc', ('Prev', '1'), '2'),
                'o1|xpath://*[@id="vendor_contracts"]/tbody/tr[2]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[3]/td[6]>>'),
                'o2|xpath://*[@id="vendor_contracts"]/tbody/tr[3]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[4]/td[6]>>'),
                'o3|xpath://*[@id="vendor_contracts"]/tbody/tr[4]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[5]/td[6]>>'),
                'o4|xpath://*[@id="vendor_contracts"]/tbody/tr[5]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[6]/td[6]>>'),
            },
            'paging': {
                'params': {'args': '008050242', 'test': 'true', 'page': 2},
                'action': ('link_text:2', 'click'),
                'naics': ('all', 27),
                'membership_filters': (None, 2, 0, 2, {
                    1: ('Shelly Bowan', '703-418-0636', 'OASIS@act-i.com'),
                    2: ('Jeff Earley', '703-418-0636', 'OASIS@act-i.com')
                }),
                'vendor_sam': ('2/13/19',),
                'vendor_info': ('ADVANCED CONCEPTS AND TECHNOLOGIES INTERNATIONAL, LLC DBA ACT-I', '008050242', '1C2H1', '55', '$5,400,000'),
                'vendor_address': ('1105 Wooded Acres Ste 500', 'Waco, TX 76710', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/008050242/csv/?page=2',),
                'contract_table': (5, 'h_date_signed', 'desc', ('2', 'Next'), '1'),
            },
            'page_count': {
                'params': {'args': '039872622', 'test': 'true', 'count': 3},
                'naics': ('all', 10),
                'membership_filters': (None, 3, 0, 2, {
                    1: ('Lynna S. Hood', '571-257-4785', 'lhood@addxcorp.com'),
                    2: ('Lynna S. Hood', '571-257-4785', 'lhood@addxcorp.com'),
                    3: ('', '703-933-7637', 'lhood@addxcorp.com')
                }, {
                    1: ('VO', 'SDVO'),
                    2: ('VO', 'SDVO')
                }),
                'vendor_sam': ('10/16/18',),
                'vendor_info': ('ADDX CORPORATION', '039872622', '1XPA3', '62', '$16,534,185'),
                'vendor_address': ('4900 Seminary Rd Ste 700', 'Alexandria, VA 22311', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/039872622/csv/?count=3',),
                'contract_table': (3, 'h_date_signed', 'desc', ('Prev', '1'), '4'),
            }
        },
        'header': {
            'params': {
                'args': '926451519'
            },
            'wait': ('text', '#site_status', 'complete'),
            'BALL AEROSPACE & TECHNOLOGIES CORPORATION - Discovery': 'title'
        },
        'vendor_info': {
            'params': {
                'args': '968706106',
                'vehicle': 'OASIS_SB',
                'naics': '541330',
                'setasides': 'A6'
            },
            'wait': ('text', '#site_status', 'complete'),
            'span.cage_code.admin_data': ('text__equal', '6HBK6'),
            'span.duns_number.admin_data': ('text__equal', '968706106'),
            'span.number_of_employees.admin_data': ('int__is_max', 445),
            'span.annual_revenue.admin_data': ('int__is_max', 48021632),
            'span.vendor_address1.admin_data2': ('text__equal', '7000 Muirkirk Meadows Dr'),
            'span.vendor_address2.admin_data2': ('text__equal', 'Beltsville, MD 20705'),
            'xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[2]/td[3]': ('text__equal', 'Benjamin W. Saunders'),
            'xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[2]/td[4]': ('text__equal', '571-266-2986'),
            'xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[2]/td[5]': ('text__equal', 'OASIS@asrcfederal.com'),
        },
        'contract_info_displayed': {
            'params': ({
                'args': '623876096',
                'vehicle': 'OASIS_SB',
                'naics': '541330'
            },{
                'args': '102067378',
                'vehicle': 'OASIS_SB',
                'naics': '541712'
            }),
            'wait': ('text', '#site_status', 'complete'),
            '#no_matching_contracts': 'not_displayed',
            'xpath://*[@id="ch_table"]/div/table/tbody/tr[2]': 'exists'
        },
        'csv_links': {
            'params': {
                'args': '626979228',
                'naics': '541620'
            },
            'wait': ('text', '#site_status', 'complete'),
            'link_text:Download vendor data (CSV)': ('link__matches', r'^[\s\S]*/vendor/[\s\S]*/csv[\s\S]*$')
        },
        'address_header': {
            'params': {
                'args': '170203199',
                'naics': '541618'
            },
            'wait': ('text', '#site_status', 'complete'),
            'p.admin_title': ('text__equal', 'Address')
        },
        'no_matching_contracts': {
            'params': {
                'args': '053117149',
                'vehicle': 'BMO_SB',
                'naics': '561730'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#no_matching_contracts': 'displayed'
        },
        'matching_contracts': {
            'params': {
                'args': '080778868',
                'vehicle': 'BMO_SB',
                'naics': '541330'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#no_matching_contracts': 'not_displayed'
        },
        'small_business_badge': {
            'params': {
                'args': '053117149',
                'vehicle': 'BMO_SB',
                'naics': '236220'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#sb_badge': 'displayed'
        },
        'no_small_business_badge': {
            'params': {
                'args': '041733197',
                'vehicle': 'HCATS',
                'naics': '541611'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#sb_badge': 'not_displayed'
        },
        'vendor_site': {
            'params': {
                'args': '168719552',
                'vehicle': 'HCATS_SB',
                'naics': '541611'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#vendor_site_link': ('link__equal', 'http://www.arcaspicio.com/')
        },
        'no_vendor_site': {
            'params': {
                'args': '626979228',
                'vehicle': 'OASIS_SB',
                'naics': '541330'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#vendor_site_link': 'not_displayed'
        },
        'contract_pagination': {
            'params': {
                'args': '926451519',
                'vehicle': 'OASIS',
                'test': 'true'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#contracts_current': ('text__equal', '1 - 5'),
            '#contracts_total': ('int__is_min', 10),
            '#pagination_container': 'displayed',
            '#viewing_contracts': 'displayed'
        },
        'no_contract_pagination': {
            'params': {
                'args': '008050242',
                'vehicle': 'OASIS_SB',
                'naics': '541611',
                'test': 'true'
            },
            'wait': ('text', '#site_status', 'complete'),
            '#pagination_container': 'not_displayed',
            '#viewing_contracts': 'displayed'
        },
        'capability_statements': {
            'params': {
                'args': '028509656',
                'vehicle': 'OASIS_SB',
                'test': 'true'
            },
            'wait': ('text', '#site_status', 'complete'),
            'xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[2]/td[2]/div/a': ('link__equal', 'http://localhost:8080/discovery_site/capability_statements/OASIS_SB/028509656.pdf') 
        }
    })
    
    def initialize(self):
        self.path = 'vendor'
