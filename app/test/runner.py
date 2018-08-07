
from django.test.runner import (
    DiscoverRunner, 
    is_discoverable, reorder_suite
)

import os


def filter_tests_by_tags(suite, tags, exclude_tags, require_all = False):
    suite_class = type(suite)
    filtered_suite = suite_class()

    for test in suite:
        if isinstance(test, suite_class):
            filtered_suite.addTests(filter_tests_by_tags(test, tags, exclude_tags, require_all))
        else:
            test_tags = set(getattr(test, 'tags', set()))
            test_fn_name = getattr(test, '_testMethodName', str(test))
            test_fn = getattr(test, test_fn_name, test)
            test_fn_tags = set(getattr(test_fn, 'tags', set()))
            all_tags = test_tags.union(test_fn_tags)
            matched_tags = []
            
            if require_all:
                matches = all_tags.intersection(tags)
                if len(tags) == len(matches):
                    matched_tags = matches
            else:
                matched_tags = all_tags.intersection(tags)
            
            if (matched_tags or not tags) and not all_tags.intersection(exclude_tags):
                filtered_suite.addTest(test)

    return filtered_suite


class DiscoveryTestRunner(DiscoverRunner):
    
    def __init__(self, pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=False, require_all=False,
                 reverse=False, debug_mode=False, debug_sql=False, parallel=0,
                 tags=None, exclude_tags=None, **kwargs):
        
        self.require_all = require_all

        super(DiscoveryTestRunner, self).__init__(
            pattern = pattern,
            top_level = top_level,
            verbosity = verbosity,
            interactive = interactive,
            failfast = failfast,
            keepdb = keepdb,
            reverse = reverse,
            debug_mode = debug_mode,
            debug_sql = debug_sql,
            parallel = parallel,
            tags = tags,
            exclude_tags = exclude_tags,
            **kwargs
        )

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument(
            '-a', '--require-all', action='store_true',
            help='Require all tags specified to run tests.'
        )
        super(DiscoveryTestRunner, cls).add_arguments(parser)

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        suite = self.test_suite()
        test_labels = test_labels or ['.']
        extra_tests = extra_tests or []

        discover_kwargs = {}
        if self.pattern is not None:
            discover_kwargs['pattern'] = self.pattern
        if self.top_level is not None:
            discover_kwargs['top_level_dir'] = self.top_level

        for label in test_labels:
            kwargs = discover_kwargs.copy()
            tests = None

            label_as_path = os.path.abspath(label)

            if not os.path.exists(label_as_path):
                tests = self.test_loader.loadTestsFromName(label)
            elif os.path.isdir(label_as_path) and not self.top_level:
                top_level = label_as_path
                while True:
                    init_py = os.path.join(top_level, '__init__.py')
                    if os.path.exists(init_py):
                        try_next = os.path.dirname(top_level)
                        if try_next == top_level:
                            break
                        top_level = try_next
                        continue
                    break
                kwargs['top_level_dir'] = top_level

            if not (tests and tests.countTestCases()) and is_discoverable(label):
                tests = self.test_loader.discover(start_dir=label, **kwargs)
                self.test_loader._top_level_dir = None

            suite.addTests(tests)

        for test in extra_tests:
            suite.addTest(test)

        if self.tags or self.exclude_tags:
            if self.verbosity >= 2:
                if self.tags:
                    print('Including test tag(s): %s.' % ', '.join(sorted(self.tags)))
                if self.exclude_tags:
                    print('Excluding test tag(s): %s.' % ', '.join(sorted(self.exclude_tags)))
            
            suite = filter_tests_by_tags(suite, self.tags, self.exclude_tags, self.require_all)
        
        suite = reorder_suite(suite, self.reorder_by, self.reverse)

        if self.parallel > 1:
            parallel_suite = self.parallel_test_suite(suite, self.parallel, self.failfast)
            parallel_units = len(parallel_suite.subsuites)
            self.parallel = min(self.parallel, parallel_units)

            if self.parallel > 1:
                suite = parallel_suite

        return suite
