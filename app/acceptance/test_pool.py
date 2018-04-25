from test import cases as case


OASIS_SB_NAICS = {
    'vehicle': 'oasis_sb',
    'naics-code': '541990'
}

OASIS_SB_NAICS_2 = {
    'vehicle': 'oasis_sb',
    'naics-code': '541620'
}

OASIS_SB_NAICS_3 = {
    'vehicle': 'oasis_sb',
    'naics-code': '541618'
}

OASIS_SB_NAICS_4 = {
    'vehicle': 'oasis_sb',
    'naics-code': '541219'
}

OASIS_SB_NAICS_WO = {
    'vehicle': 'oasis_sb',
    'naics-code': '541330',
    'setasides': 'A2'
}

OASIS_SB_NAICS_8A = {
    'vehicle': 'oasis_sb',
    'naics-code': '541330B',
    'setasides': 'A6'
}

OASIS_SB_NAICS_8A_2 = {
    'vehicle': 'oasis_sb',
    'naics-code': '541612',
    'setasides': 'A6'
}

OASIS_SB_NAICS_HZ = {
    'vehicle': 'oasis_sb',
    'naics-code': '541330',
    'setasides': 'XX'
}

OASIS_NAICS = {
    'vehicle': 'oasis',
    'naics-code': '541990'
}

OASIS_NAICS_2 = {
    'vehicle': 'oasis',
    'naics-code': '541618'
}


class PoolTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = {
        'header': {
            'Discovery': 'title'
        },
        'search_veteran_owned': {
            'params': OASIS_SB_NAICS,
            'wait': ('class', 'table_row_data'),
            'actions': {
                'vet*click': {
                    'wait': ('id', 'your_filters', 'Veteran Owned'),
                    'your_filters': ('text__equal', 'Veteran Owned'),
                    'css:span.matching_your_search': ('text__matches', r'^[\s\S]* vendors match your search$')
                }
            }
        },
        'search_zero_results': {
            'params': {
                'vehicle': 'oasis_sb',
                'naics-code': '541990',
                'setasides': ('A6', 'A2', 'XX')
            },
            'wait': ('sec', 2),
            'css:span.matching_your_search': ('text__equal', '0 vendors match your search')
        },
        'search_socioeconomic_indicators': {
            'params': OASIS_SB_NAICS_WO,
            'wait': ('class', 'table_row_data'),
            'woman': ('value__equal', 'A2'),
            'css:th.h_8a': ('text__equal', '8(a)'),
            'css:th.h_hubz': ('text__equal', 'HubZ'),
            'css:th.h_sdvo': ('text__equal', 'SDVO'),
            'css:th.h_wo': ('text__equal', 'WO'),
            'css:th.h_vo': ('text__equal', 'VO'),
            'css:th.h_sdb': ('text__equal', 'SDB'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[7]/img': 'exists'
        },
        'search_result_count': {
            'params': OASIS_SB_NAICS_WO,
            'wait': ('class', 'table_row_data'),
            'css:span.matching_your_search': ('text__equal', '1 vendors match your search')
        },
        'search_result_criteria': {
            'params': OASIS_SB_NAICS_WO,
            'wait': ('class', 'table_row_data'),
            'your_search': ('text__equal', 'Engineering Services')
        },
        'search_vendor_count': {
            'params': OASIS_SB_NAICS_WO,
            'wait': ('class', 'table_row_data'),
            'css:span.matching_your_search': ('text__matches', r'\d+ vendors match your search')
        },
        '8a_added': {
            'params': OASIS_SB_NAICS_8A,
            'wait': ('class', 'table_row_data'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[4]/img': 'exists'
        },
        'hubzone_added': {
            'params': OASIS_SB_NAICS_HZ,
            'wait': ('class', 'table_row_data'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[5]/img': 'exists'
        },
        'search_pool_number_not_displayed': {
            'params': OASIS_SB_NAICS_8A_2,
            'wait': ('class', 'table_row_data'),
            'css:span.matching_your_search': ('text__matches', r'^[\s\S]* vendors match your search$')
        },
        'csv_link': {
            'params': OASIS_SB_NAICS_2,
            'wait': ('class', 'table_row_data'),
            'link_text:download data (CSV)': ('link__matches', r'^[\s\S]*/results/csv[\s\S]*$')
        },
        'vehicle_naics_select_order': {
            'params': OASIS_SB_NAICS_3,
            'wait': ('class', 'table_row_data'),
            'naics-code': 'enabled',
            'placeholder': 'enabled',
            'css:.se_filter': 'enabled'
        },
        'unrestricted_socioeconomic_factors': {
            'params': OASIS_NAICS_2,
            'wait': ('class', 'vendor_name'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[4]': ('text__equal', '8(a)'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[5]': ('text__equal', 'HubZ'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[6]': ('text__equal', 'SDVO'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[7]': ('text__equal', 'WO'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[8]': ('text__equal', 'VO'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[9]': ('text__equal', 'SDB'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[4]': ('text__equal', 'Not Applicable\n(SB Only)'),
            'choose_filters': ('text__equal', 'Choose filters (SB Only)'),
            'css:.se_filter': 'disabled'
        },
        'contract_count_column': {
            'params': OASIS_SB_NAICS_4,
            'wait': ('class', 'vendor_name'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[1]/th[3]': ('text__equal', 'Contracts'),
            'xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[3]': ('int__is_above', '<<xpath://*[@id="pool_vendors"]/tbody/tr[3]/td[3]>>')
        }
    }
    
    def initialize(self):
        self.path = 'results'
