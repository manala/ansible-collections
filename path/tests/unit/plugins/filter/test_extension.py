from __future__ import annotations

import unittest
from plugins.filter.extension import _extension as _filter_extension

from ansible.errors import AnsibleTemplateError


class TestExtension(unittest.TestCase):

    def test_invalid_input(self):
        paths = NotImplemented
        extension = 'foo'

        with self.assertRaisesRegex(AnsibleTemplateError, f'extension input expects a dict but was given a {type(paths).__name__}'):
            _filter_extension(paths, extension)

        with self.assertRaisesRegex(AnsibleTemplateError, f'extension input expects a dict but was given a {type(paths).__name__}'):
            _filter_extension([paths], extension)

    def test_invalid_extension(self):
        paths = {'path': 'path'}
        extension = NotImplemented

        with self.assertRaisesRegex(AnsibleTemplateError, f'extension option expects a string but was given a {type(extension).__name__}'):
            _filter_extension(paths, extension)

        with self.assertRaisesRegex(AnsibleTemplateError, f'extension option expects a string but was given a {type(extension).__name__}'):
            _filter_extension([paths], extension)

    def test(self):
        self.assertEqual({
            'path': 'path.foo',
        }, _filter_extension(
            {'path': 'path'},
            'foo',
        ))

    def test_dotted_extension(self):
        self.assertEqual({
            'path': 'path.foo',
        }, _filter_extension(
            {'path': 'path'},
            '.foo',
        ))

    def test_path_already_extensioned(self):
        self.assertEqual({
            'path': 'path.foo',
        }, _filter_extension(
            {'path': 'path.foo'},
            'foo',
        ))
