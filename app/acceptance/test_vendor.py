from test import cases as case


class VendorTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
        'header': {
            'params': {
                'args': '926451519'
            },
            'wait': ('sec', 1),
            'Ball Aerospace & Technologies Corporation - Discovery': 'title'
        },
        'vendor_info': {
            'params': {
                'args': '170203199',
                'vehicle': 'OASIS_SB',
                'naics': '541330',
                'setasides': 'A6'
            },
            'wait': ('class', 'table_row_data'),
            'span.cage_code.admin_data': ('text__equal', '35CZ6'),
            'span.duns_number.admin_data': ('text__equal', '170203199'),
            'span.number_of_employees.admin_data': ('int__is_max', 62),
            'span.annual_revenue.admin_data': ('int__is_max', 5686000),
            'span.vendor_address1.admin_data2': ('text__equal', '8610 Explorer Dr Ste 305'),
            'span.vendor_address2.admin_data2': ('text__equal', 'Colorado Springs, CO 80920'),
            'xpath://*[@id="contact_details"]/tbody/tr[2]/td[3]': ('text__equal', 'Denise Penn'),
            'xpath://*[@id="contact_details"]/tbody/tr[2]/td[4]': ('text__equal', '719-418-4968'),
            'xpath://*[@id="contact_details"]/tbody/tr[2]/td[5]': ('text__equal', 'OASISPOOL1@apogeemail.net'),
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
            'wait': ('class', 'table_row_data'),
            '#no_matching_contracts': 'not_displayed',
            'xpath://*[@id="ch_table"]/div/table/tbody/tr[2]': 'exists'
        },
        'csv_links': {
            'params': {
                'args': '626979228',
                'naics': '541620'
            },
            'wait': ('sec', 2),
            'link_text:Download vendor data (CSV)': ('link__matches', r'^[\s\S]*/vendor/[\s\S]*/csv[\s\S]*$')
        },
        'address_header': {
            'params': {
                'args': '786997739',
                'naics': '541618'
            },
            'wait': ('sec', 1),
            'p.admin_title': ('text__equal', 'Address')
        },
        'no_matching_contracts': {
            'params': {
                'args': '053117149',
                'vehicle': 'BMO_SB',
                'naics': '561730'
            },
            'wait': ('sec', 2),
            '#no_matching_contracts': 'displayed'
        },
        'matching_contracts': {
            'params': {
                'args': '080778868',
                'vehicle': 'BMO_SB',
                'naics': '541330'
            },
            'wait': ('sec', 2),
            '#no_matching_contracts': 'not_displayed'
        },
        'small_business_badge': {
            'params': {
                'args': '053117149',
                'vehicle': 'BMO_SB',
                'naics': '236220'
            },
            'wait': ('class', 'table_row_data'),
            '#sb_badge': 'displayed'
        },
        'no_small_business_badge': {
            'params': {
                'args': '041733197',
                'vehicle': 'HCATS',
                'naics': '541611'
            },
            'wait': ('class', 'table_row_data'),
            '#sb_badge': 'not_displayed'
        },
        'vendor_site': {
            'params': {
                'args': '168719552',
                'vehicle': 'HCATS_SB',
                'naics': '541611'
            },
            'wait': ('class', 'table_row_data'),
            '#vendor_site_link': ('link__equal', 'http://www.arcaspicio.com/')
        },
        'no_vendor_site': {
            'params': {
                'args': '626979228',
                'vehicle': 'OASIS_SB',
                'naics': '541330'
            },
            'wait': ('class', 'table_row_data'),
            '#vendor_site_link': 'not_displayed'
        },
        'contract_pagination': {
            'params': {
                'args': '926451519',
                'vehicle': 'OASIS',
                'test': 'true'
            },
            'wait': ('class', 'agency'),
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
            'wait': ('class', 'agency'),
            '#pagination_container': 'not_displayed',
            '#viewing_contracts': 'displayed'
        },
        'capability_statements': {
            'params': {
                'args': '028509656',
                'vehicle': 'OASIS_SB',
                'test': 'true'
            },
            'wait': ('class', 'capability_statement_link'),
            'xpath://*[@id="vendor_contact_table_container"]/div/form/table/tbody/tr[2]/td[2]/div/a': ('link__equal', 'http://localhost:8080/discovery_site/capability_statements/OASIS_SB/028509656.pdf') 
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
            'vehicle': 'OASIS_SB', 
            'naics': '541330'
        })
