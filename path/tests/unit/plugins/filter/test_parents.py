from __future__ import annotations

import unittest
from plugins.filter.parents import _parents as _filter_parents


class TestParents(unittest.TestCase):

    def test(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'foo/bar'},
            {'path': 'foo/bar/baz', 'mode': 123},
        ], _filter_parents([
            {'path': 'foo/bar/baz', 'mode': 123},
        ]))

    def test_duplicate(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'foo/bar'},
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar', 'mode': 123},
        ], _filter_parents([
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar', 'mode': 123},
        ]))

    def test_multiple(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'foo/bar'},
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar/qux', 'mode': 123},
            {'path': 'foo/qux'},
            {'path': 'foo/qux/quux', 'mode': 123},
        ], _filter_parents([
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar/qux', 'mode': 123},
            {'path': 'foo/qux/quux', 'mode': 123},
        ]))

    def test_multiple_normalize(self):
        self.assertEqual([
            {'path': 'foo'},
            {'path': 'foo/bar'},
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar/../bar/qux', 'mode': 123},
            {'path': 'foo/qux'},
            {'path': 'foo/qux/qux/../quux', 'mode': 123},
        ], _filter_parents([
            {'path': 'foo/bar/baz', 'mode': 123},
            {'path': 'foo/bar/../bar/qux', 'mode': 123},
            {'path': 'foo/qux/qux/../quux', 'mode': 123},
        ]))
