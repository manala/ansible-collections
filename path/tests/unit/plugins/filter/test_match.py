from __future__ import annotations

import unittest
from plugins.filter.match import _match as _filter_match


class TestMatch(unittest.TestCase):

    def test(self):
        paths = [
            {'path': '/foo'},
            {'path': '/foo/bar'},
            {'path': '/foo/bar/baz'},
        ]
        pattern = '*baz'

        self.assertEqual([
            {'path': '/foo/bar/baz'},
        ], _filter_match(paths, pattern))
