from test import cases as case
from test import fixtures as data


class SetAsideTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            '&A5': ('name', 'exact', 'VO'),
            '&XX': ('name', 'exact', 'HubZ'),
            '&A2': ('name', 'exact', 'WO'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': ('code', 'name', 'description', 'far_order'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 3},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 2}
        },
        'search': {
            '@search1': ('description', 'regex', 'Veteran'),
            '*search2': ('name', 'exact', 'SDB'),
            '-search3': ('code', 'regex', '0000000000000')
        },
        'fields': {
            'code': {
                '*exact': 'QF',
                '*iexact': 'a2',
                '@in': ('XX', 'A5', '27')
            },
            'name': {
                '*exact': 'WO',
                '*iexact': 'hubz',
                '@in': ('8(A)', 'SDVO', 'HubZ')
            },
            'description': {
                '*exact': 'Veteran Owned',
                '*iexact': 'hubzone',
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
            'far_order': {
                '@exact': 3,
                '@lt': 4,
                '@lte': 4, 
                '@gt': 3, 
                '@gte': 3,
                '@range': (2, 5),
                '@in': (2, 3, 5)
            }
        },
        'requests': {
            '@r1': {
                'params': {'q': 'Dis', 'ordering': '-name'},
                'tests': (
                    ('description', 'regex', 'Dis'),
                    ('name', 'ordering', 'desc')
                )
            },
            '*r2': {
                'params': {'q': 'QF', 'ordering': '-code'},
                'tests': (
                    ('code', 'exact', 'QF'),
                    ('code', 'ordering', 'desc')
                )
            },
            '@r3': {
                'params': {'q': 'Owned', 'ordering': 'far_order'},
                'tests': (
                    ('description', 'regex', 'Owned'),
                    ('far_order', 'ordering', 'asc')
                )
            },
            '-r4': {
                'params': {'q': 'Space Man', 'ordering': 'code'}
            },
            '-r5': {
                'params': {'q': 'Arghhhhh!!', 'ordering': '-description'}
            }
        }
    }


    def initialize(self):
        self.router = 'setasides'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['name'])
        resp.is_not_empty(base_key + ['description'])
        resp.is_int(base_key + ['far_order'])
