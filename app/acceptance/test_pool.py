from django.test import tag

from test import cases as case

from acceptance.common import generate_schema
from acceptance.search import generate_search_tests


@tag('search')
class PoolTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
    
    schema = generate_schema({
        'includes': {
            'search': generate_search_tests()
        },
        'header': {
            'tags': ('info', 'title'),
            'wait': 'complete',
            'Results - Discovery': 'title'
        },
        'actions': {
            'unfiltered': {
                'tags': ('all',),
                'naics': ('all', 78, True),
                'vehicle': ('all', 8, True),
                'pool': ('all', 60, 59, True),
                'zone': ('', 6, False, False),
                'setaside_filters': (None, 0, True),
                'vendor_result_info': (192, 'results/csv/?'),
                'vendor_table': (50, 'h_naics_results', 'desc', ('Prev', '1'), '4')
            },
            'pool_links': {
                'tags': ('pool', 'link', 'bmo_sb'),
                'params': {'vehicle': 'BMO_SB', 'pools': 'BMO_SB_1'},
                'action': ('#link_BMO_SB_1', 'click'),
                'naics': ('all', 3, True),
                'vehicle': ('BMO_SB', 8, True),
                'pool': ('BMO_SB_1', 17, 1, True),
                'zone': ('', 6, True, True),
                'setaside_filters': (None, 0, True),
                'vendor_result_info': (10, 'results/csv/?vehicle=BMO_SB&pools=BMO_SB_1&'),
                'vendor_table': (10, 'h_naics_results', 'desc')
            },
            'sorting': {
                'tags': ('sort',),
                'params': {'ordering': 'name'},
                'action': (('th.h_vendor_name', 'click'), ('th.h_vendor_name', 'click')),
                'naics': ('all', 78, True),
                'vehicle': ('all', 8, True),
                'pool': ('all', 60, 59, True),
                'zone': ('', 6, False, False),
                'setaside_filters': (None, 0, True),
                'vendor_result_info': (192, 'results/csv/?ordering=name'),
                'vendor_table': (50, 'h_vendor_name', 'asc', ('Prev', '1'), '4'),
                'o1|xpath://*[@id="pool_vendors"]/tbody/tr[2]/td[1]': ('text__is_max', '<<xpath://*[@id="pool_vendors"]/tbody/tr[10]/td[1]>>'),
                'o2|xpath://*[@id="pool_vendors"]/tbody/tr[10]/td[1]': ('text__is_max', '<<xpath://*[@id="pool_vendors"]/tbody/tr[20]/td[1]>>'),
                'o3|xpath://*[@id="pool_vendors"]/tbody/tr[20]/td[1]': ('text__is_max', '<<xpath://*[@id="pool_vendors"]/tbody/tr[30]/td[1]>>'),
                'o4|xpath://*[@id="pool_vendors"]/tbody/tr[30]/td[1]': ('text__is_max', '<<xpath://*[@id="pool_vendors"]/tbody/tr[40]/td[1]>>'),
                'o5|xpath://*[@id="pool_vendors"]/tbody/tr[40]/td[1]': ('text__is_max', '<<xpath://*[@id="pool_vendors"]/tbody/tr[50]/td[1]>>')
            },
            'paging': {
                'tags': ('page',),
                'params': {'page': 3},
                'action': ('link_text:3', 'click'),
                'naics': ('all', 78, True),
                'vehicle': ('all', 8, True),
                'pool': ('all', 60, 59, True),
                'zone': ('', 6, False, False),
                'setaside_filters': (None, 0, True),
                'vendor_result_info': (192, 'results/csv/?'),
                'vendor_table': (50, 'h_naics_results', 'desc', '3', '4')
            },
            'page_count': {
                'tags': ('page',),
                'params': {'count': 10},
                'naics': ('all', 78, True),
                'vehicle': ('all', 8, True),
                'pool': ('all', 60, 59, True),
                'zone': ('', 6, False, False),
                'setaside_filters': (None, 0, True),
                'vendor_result_info': (192, 'results/csv/?'),
                'vendor_table': (10, 'h_naics_results', 'desc', ('Prev', '1'), '4')
            }
        }
    })
    
    def initialize(self):
        self.path = 'results'
