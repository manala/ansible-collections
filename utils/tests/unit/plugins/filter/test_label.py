from __future__ import annotations

import unittest
from plugins.filter.label import _label as _filter_label

from ansible.errors import AnsibleTemplateError


class TestLabel(unittest.TestCase):

    def test_invalid_input(self):
        data = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_label(data)
        self.assertEqual(f'label input expects a dict but was given a {type(data).__name__}', str(error.exception))

    def test(self):
        self.assertEqual(
            {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
            )
        )

    def test_keep(self):
        self.assertEqual(
            {'foo': 'foo'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                keep=['foo'],
            )
        )

    def test_keep_remove(self):
        self.assertEqual(
            {},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                keep=['foo'],
                remove=['foo'],
            )
        )

    def test_remove(self):
        self.assertEqual(
            {'bar': 'bar', 'baz': 'baz'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                remove=['foo'],
            )
        )

    def test_mask(self):
        self.assertEqual(
            {'foo': '<masked>', 'bar': 'bar', 'baz': 'baz'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                mask=['foo'],
            )
        )

    def test_mask_keep(self):
        self.assertEqual(
            {'foo': '<masked>'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                mask=['foo'],
                keep=['foo'],
            )
        )
        self.assertEqual(
            {'foo': '<masked>', 'bar': 'bar'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                mask=['foo'],
                keep=['bar'],
            )
        )

    def test_mask_remove(self):
        self.assertEqual(
            {'bar': 'bar', 'baz': 'baz'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                mask=['foo'],
                remove=['foo'],
            )
        )
        self.assertEqual(
            {'foo': '<masked>', 'baz': 'baz'},
            _filter_label(
                {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
                mask=['foo'],
                remove=['bar'],
            )
        )
