from __future__ import annotations

import unittest
from plugins.filter.state import _state as _filter_state

from ansible.errors import AnsibleTemplateError


class TestLabel(unittest.TestCase):

    def test_invalid_inputs(self):
        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_state(NotImplemented)
        self.assertEqual('state input expects a dict but was given a NotImplementedType', str(error.exception))

    def test_empty(self):
        self.assertEqual(
            'directory',
            _filter_state({})
        )

    def test_explicit(self):
        self.assertEqual(
            'absent',
            _filter_state({'path': 'path', 'state': 'absent'})
        )
        self.assertEqual(
            'file',
            _filter_state({'path': 'path', 'state': 'file'})
        )
        self.assertEqual(
            'directory',
            _filter_state({'path': 'path', 'state': 'directory'})
        )
        self.assertEqual(
            'link',
            _filter_state({'path': 'path', 'state': 'link'})
        )

    def test_implicit_file(self):
        self.assertEqual(
            'file',
            _filter_state({'path': 'path', 'content': 'content'})
        )
        self.assertEqual(
            'file',
            _filter_state({'path': 'path', 'file': 'file'})
        )
        self.assertEqual(
            'file',
            _filter_state({'path': 'path', 'template': 'template'})
        )

    def test_implicit_link(self):
        self.assertEqual(
            'link',
            _filter_state({'path': 'path', 'src': 'src'})
        )

    def test_implicit_directory(self):
        self.assertEqual(
            'directory',
            _filter_state({'path': 'path'})
        )
