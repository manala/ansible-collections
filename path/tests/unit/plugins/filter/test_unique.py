from __future__ import annotations

import unittest
from plugins.filter.unique import _unique as _filter_unique


class TestUnique(unittest.TestCase):

    def test(self):
        self.assertEqual([
            {'path': 'foo'},
        ], _filter_unique([
            {'path': 'foo'},
            {'path': 'foo'},
        ]))

    def test_normalize(self):
        self.assertEqual([
            {'path': 'foo'},
        ], _filter_unique([
            {'path': 'bar/../foo'},
            {'path': 'foo'},
        ]))

    def test_pick_first_place_first(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 111},
            {'path': 'bar'},
            {'path': 'baz'},
        ], _filter_unique([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 111},
            {'path': 'bar'},
            {'path': 'qux', 'mode': 222},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 333},
        ], pick='first', place='first'))

    def test_pick_first_place_last(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'bar'},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 111},
        ], _filter_unique([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 111},
            {'path': 'bar'},
            {'path': 'qux', 'mode': 222},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 333},
        ], pick='first', place='last'))

    def test_pick_last_place_first(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 333},
            {'path': 'bar'},
            {'path': 'baz'},
        ], _filter_unique([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 111},
            {'path': 'bar'},
            {'path': 'qux', 'mode': 222},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 333},
        ], pick='last', place='first'))

    def test_pick_last_place_last(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'bar'},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 333},
        ], _filter_unique([
            {'path': 'foo'},
            {'path': 'qux', 'mode': 111},
            {'path': 'bar'},
            {'path': 'qux', 'mode': 222},
            {'path': 'baz'},
            {'path': 'qux', 'mode': 333},
        ], pick='last', place='last'))
