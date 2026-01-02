from __future__ import annotations

import unittest
from plugins.filter.parse import _parse as _filter_parse

from ansible.errors import AnsibleTemplateError


class TestParse(unittest.TestCase):

    def test_invalid_inputs(self):
        path = NotImplemented

        with self.assertRaisesRegex(AnsibleTemplateError, f'parse input expects a dict but was given a {type(path).__name__}'):
            _filter_parse(path)

    def test(self):
        self.assertEqual({
            'parent': '',
            'name': '',
            'stem': '',
            'extension': '',
        } , _filter_parse(
            {'path': ''}
        ))

        self.assertEqual({
            'parent': '',
            'name': 'foo',
            'stem': 'foo',
            'extension': '',
        } , _filter_parse(
            {'path': 'foo'}
        ))

        self.assertEqual({
            'parent': '',
            'name': 'foo.bar',
            'stem': 'foo',
            'extension': 'bar',
        } , _filter_parse(
            {'path': 'foo.bar'}
        ))

        self.assertEqual({
            'parent': '',
            'name': 'foo',
            'stem': 'foo',
            'extension': '',
        } , _filter_parse(
            {'path': '/foo'}
        ))

        self.assertEqual({
            'parent': '',
            'name': 'foo.bar',
            'stem': 'foo',
            'extension': 'bar',
        } , _filter_parse(
            {'path': '/foo.bar'}
        ))

        self.assertEqual({
            'parent': '/foo/bar',
            'name': 'baz',
            'stem': 'baz',
            'extension': '',
        } , _filter_parse(
            {'path': '/foo/bar/baz'}
        ))

        self.assertEqual({
            'parent': '/foo/bar',
            'name': 'baz.qux',
            'stem': 'baz',
            'extension': 'qux',
        } , _filter_parse(
            {'path': '/foo/bar/baz.qux'}
        ))
