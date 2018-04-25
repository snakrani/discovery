from test import cases as case


class VendorTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
        'header': {
            'params': {
                'args': '926451519'
            },
            'Ball Aerospace & Technologies Corporation - Discovery': 'title'
        },
        'vendor_info': {
            'params': {
                'args': '170203199',
                'vehicle': 'oasis_sb',
                'naics-code': '541330',
                'setasides': 'A6'
            },
            'wait': ('class', 'table_row_data'),
            'css:span.cage_code.admin_data': ('text__equal', '35CZ6'),
            'css:span.duns_number.admin_data': ('text__equal', '170203199'),
            'css:span.number_of_employees.admin_data': ('int__is_max', 62),
            'css:span.annual_revenue.admin_data': ('int__is_max', 5686000),
            'css:span.vendor_address1.admin_data2': ('text__equal', '8610 Explorer Dr Ste 305'),
            'css:span.vendor_address2.admin_data2': ('text__equal', 'Colorado Springs, CO 80920'),
            'css:span.vendor_poc_name.admin_data2': ('text__equal', 'Bobby P. Veazey'),
            'css:span.vendor_poc_phone.admin_data2': ('text__equal', '719-213-6199'),
            'css:span.vendor_poc_email.admin_data2': ('text__equal', 'OASISPOOL1@apogeemail.net'),
        },
        'all_contracts_button': {
            'params': {
                'args': '118498067',
                'vehicle': 'oasis_sb',
                'naics-code': '541330C'
            },
            'wait': ('class', 'table_row_data'),
            'all_contracts_button': ('text__equal', 'All Contracts'),
            'naics_contracts_button': ('text__equal', 'NAICS 541330'),
            'actions': {
                'all_contracts_button*click': {
                    'wait': ('sec', 2),
                    'all_contracts_button': ('has_class', 'contracts_button_active')
                }
            }
        },
        'naics_contracts_button': {
            'params': {
                'args': '049192649',
                'vehicle': 'oasis_sb',
                'naics-code': '541330'
            },
            'wait': ('class', 'table_row_data'),
            'naics_contracts_button': ('text__equal', 'NAICS 541330'),
            'all_contracts_button': ('text__equal', 'All Contracts'),
            'actions': {
                'naics_contracts_button*click': {
                    'wait': ('sec', 2),
                    'naics_contracts_button': ('has_class', 'active')
                }
            }
        },
        'contract_info_displayed': {
            'params': ({
                'args': '623876096',
                'vehicle': 'oasis_sb',
                'naics-code': '541330'
            },{
                'args': '102067378',
                'vehicle': 'oasis_sb',
                'naics-code': '541712B'
            }),
            'wait': ('class', 'table_row_data'),
            'no_matching_contracts': 'not_displayed',
            'xpath://*[@id="ch_table"]/div/table/tbody/tr[2]': 'exists'
        },
        'csv_links': {
            'params': {
                'args': '626979228',
                'naics-code': '541620'
            },
            'wait': ('sec', 2),
            'link_text:Download vendor data (CSV)': ('link__matches', r'^[\s\S]*/vendor/[\s\S]*/csv[\s\S]*$')
        },
        'poc_header': {
            'params': {
                'args': '786997739',
                'naics-code': '541618'
            },
            'wait': ('sec', 1),
            'css:p.admin_title': ('text__equal', 'POC')
        },
        'no_matching_contracts': {
            'params': {
                'args': '053117149',
                'vehicle': 'bmo_sb',
                'naics-code': '561730B'
            },
            'wait': ('sec', 2),
            'no_matching_contracts': 'displayed'
        },
        'matching_contracts': {
            'params': {
                'args': '080778868',
                'vehicle': 'bmo_sb',
                'naics-code': '541330D'
            },
            'wait': ('sec', 2),
            'no_matching_contracts': 'not_displayed'
        },
        'small_business_badge': {
            'params': {
                'args': '053117149',
                'vehicle': 'bmo_sb',
                'naics-code': '236220'
            },
            'wait': ('class', 'table_row_data'),
            'sb_badge': 'displayed'
        },
        'no_small_business_badge': {
            'params': {
                'args': '041733197',
                'vehicle': 'hcats',
                'naics-code': '541611'
            },
            'wait': ('class', 'table_row_data'),
            'sb_badge': 'not_displayed'
        },
        'vendor_site': {
            'params': {
                'args': '168719552',
                'vehicle': 'hcats_sb',
                'naics-code': '541611'
            },
            'wait': ('class', 'table_row_data'),
            'vendor_site_link': ('link__equal', 'http://www.arcaspicio.com/')
        },
        'no_vendor_site': {
            'params': {
                'args': '626979228',
                'vehicle': 'oasis_sb',
                'naics-code': '541330'
            },
            'wait': ('class', 'table_row_data'),
            'vendor_site_link': 'not_displayed'
        },
        'contract_pagination': {
            'params': {
                'args': '926451519',
                'vehicle': 'oasis',
                'test': 'true'
            },
            'wait': ('class', 'agency'),
            'contracts_current': ('text__equal', '1 - 5'),
            'contracts_total': ('int__is_min', 10),
            'pagination_container': 'displayed',
            'viewing_contracts': 'displayed'
        },
        'no_contract_pagination': {
            'params': {
                'args': '097967608',
                'vehicle': 'oasis_sb',
                'naics-code': '541330',
                'test': 'true'
            },
            'wait': ('class', 'agency'),
            'pagination_container': 'not_displayed',
            'viewing_contracts': 'displayed'
        }
    }
    
    def initialize(self):
        self.path = 'vendor'


    def test_contract_sort(self):
        
        def sort(resp):
            resp.wait_for_class('table_row_data')
            
            data_row = resp.element('xpath://*[@id="ch_table"]/div/table/tbody/tr[4]')
            resp.execute('class:h_value', 'click')
            resp.wait_for_stale(data_row)
            
            rows = resp.elements('xpath://*[@id="ch_table"]/div/table/tbody/tr')
            prev_value = None
            
            for row in rows[1:]:
                cell = resp.element('class:value', row)
                value = resp.attr(cell, 'innerText')
                
                if value:
                    value = resp.format_float(value)

                    if not prev_value:
                        prev_value = value
                    else:
                        resp.is_max(value, prev_value)
                        prev_value = value
        
        self.fetch_page(sort, **{
            'args': '049192649', 
            'vehicle': 'oasis_sb', 
            'naics-code': '541330'
        })
