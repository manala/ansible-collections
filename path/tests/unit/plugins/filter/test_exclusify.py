from __future__ import annotations

import unittest
from plugins.filter.exclusify import _exclusify as _filter_exclusify


class TestExclusify(unittest.TestCase):

    def test(self):
        self.assertEqual(
            [
                {'path': 'foo'},
                {'path': 'bar'},
                {'path': 'baz'},
                {'path': 'baz/../qux'},
                {'path': 'quux', 'state': 'absent'},
            ],
            _filter_exclusify(
                [
                    {'path': 'foo'},
                    {'path': 'bar'},
                    {'path': 'baz'},
                    {'path': 'baz/../qux'},
                ],
                [
                    {'path': 'bar'},
                    {'path': 'bar/../baz'},
                    {'path': 'qux'},
                    {'path': 'quux'},
                ],
            )
        )
