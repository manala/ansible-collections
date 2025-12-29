from __future__ import annotations

import unittest
from plugins.filter.default import _default as _filter_default

from ansible.errors import AnsibleTemplateError


class TestDefault(unittest.TestCase):

    def test_invalid_input(self):
        data = NotImplemented
        defaults = {}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default(data, defaults)
        self.assertEqual(f'default input expects a dict but was given a {type(data).__name__}', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default([data], defaults)
        self.assertEqual(f'default input expects a dict but was given a {type(data).__name__}', str(error.exception))

    def test_invalid_defaults(self):
        data = {'foo': 'bar'}
        defaults = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default(data, defaults)
        self.assertEqual(f'default options expects dicts but was given a {type(defaults).__name__}', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default([data], defaults)
        self.assertEqual(f'default options expects dicts but was given a {type(defaults).__name__}', str(error.exception))

    def test(self):
        defaults = {'bar': 'bar', 'baz': 'baz'}

        data = {'foo': 'foo', 'bar': 'foo'}

        self.assertEqual(
            {'foo': 'foo', 'bar': 'foo', 'baz': 'baz'},
            _filter_default(data, defaults),
        )

        data = [
            {'foo': 'foo', 'bar': 'foo'},
            {'foo': 'foo', 'baz': 'bar'},
        ]

        self.assertEqual([
            {'foo': 'foo', 'bar': 'foo', 'baz': 'baz'},
            {'foo': 'foo', 'bar': 'bar', 'baz': 'bar'},
        ], _filter_default(data, defaults),
        )

    def test_multiple(self):
        defaults = [
            {'bar': 'bar', 'baz': 'baz'},
            {'baz': 'baz', 'qux': 'qux'},
        ]

        data = {'foo': 'foo', 'bar': 'foo'}

        self.assertEqual(
            {'foo': 'foo', 'bar': 'foo', 'baz': 'baz', 'qux': 'qux'},
            _filter_default(data, *defaults),
        )

        data = [
            {'foo': 'foo', 'bar': 'foo'},
            {'foo': 'foo', 'baz': 'bar'},
        ]

        self.assertEqual([
            {'foo': 'foo', 'bar': 'foo', 'baz': 'baz', 'qux': 'qux'},
            {'foo': 'foo', 'bar': 'bar', 'baz': 'bar', 'qux': 'qux'},
        ], _filter_default(data, *defaults),
        )
