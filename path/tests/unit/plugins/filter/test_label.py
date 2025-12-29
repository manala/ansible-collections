from __future__ import annotations

import unittest
from plugins.filter.label import _label as _filter_label

from ansible.errors import AnsibleTemplateError


class TestLabel(unittest.TestCase):

    def test_invalid_inputs(self):
        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_label(NotImplemented)
        self.assertEqual('label input expects a dict but was given a NotImplementedType', str(error.exception))

    def test_file_implicit(self):
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'user', 'group': 'group', 'mode': 'mode'},
            _filter_label(
                {'path': 'path', 'content': 'content', 'user': 'user', 'group': 'group', 'mode': 'mode'}
            )
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'file': 'file', 'user': 'user', 'group': 'group', 'mode': 'mode'},
            _filter_label(
                {'path': 'path', 'file': 'file', 'user': 'user', 'group': 'group', 'mode': 'mode'}
            )
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'template': 'template', 'user': 'user', 'group': 'group', 'mode': 'mode'},
            _filter_label(
                {'path': 'path', 'template': 'template', 'user': 'user', 'group': 'group', 'mode': 'mode'}
            )
        )

    def test_link_implicit(self):
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'src': 'src', 'user': 'user', 'group': 'group'},
            _filter_label(
                {'path': 'path', 'src': 'src', 'user': 'user', 'group': 'group'}
            )
        )

    def test_directory_implicit(self):
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'user', 'group': 'group', 'mode': 'mode'},
            _filter_label(
                {'path': 'path', 'user': 'user', 'group': 'group', 'mode': 'mode'}
            )
        )
