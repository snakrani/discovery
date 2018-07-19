from test import cases as case


class VendorTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
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
