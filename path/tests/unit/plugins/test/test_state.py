from __future__ import annotations

import unittest
from plugins.test.state import _file as _test_file
from plugins.test.state import _link as _test_link
from plugins.test.state import _directory as _test_directory

from ansible.errors import AnsibleTemplateError


class TestFile(unittest.TestCase):

    def test_invalid_input(self):
        path = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _test_file(path)
        self.assertEqual('file expects a dict but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _test_link(path)
        self.assertEqual('link expects a dict but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _test_directory(path)
        self.assertEqual('directory expects a dict but was given a NotImplementedType', str(error.exception))

    def test_empty(self):
        path = {}

        self.assertEqual(False, _test_file(path))
        self.assertEqual(False, _test_link(path))
        self.assertEqual(True, _test_directory(path))

    def test_explicit(self):
        path_absent = {'path': 'path', 'state': 'absent'}
        path_file = {'path': 'path', 'state': 'file'}
        path_link = {'path': 'path', 'state': 'link'}
        path_directory = {'path': 'path', 'state': 'directory'}

        self.assertEqual(False, _test_file(path_absent))
        self.assertEqual(True, _test_file(path_file))
        self.assertEqual(False, _test_file(path_link))
        self.assertEqual(False, _test_file(path_directory))

        self.assertEqual(False, _test_link(path_absent))
        self.assertEqual(False, _test_link(path_file))
        self.assertEqual(True, _test_link(path_link))
        self.assertEqual(False, _test_link(path_directory))

        self.assertEqual(False, _test_directory(path_absent))
        self.assertEqual(False, _test_directory(path_file))
        self.assertEqual(False, _test_directory(path_link))
        self.assertEqual(True, _test_directory(path_directory))

    def test_implicit_file(self):
        path_content = {'path': 'path', 'content': 'content'}
        path_content_none = {'path': 'path', 'content': None}
        path_file = {'path': 'path', 'file': 'file'}
        path_file_none = {'path': 'path', 'file': None}
        path_template = {'path': 'path', 'template': 'template'}
        path_template_none = {'path': 'path', 'template': None}

        self.assertEqual(True, _test_file(path_content))
        self.assertEqual(False, _test_file(path_content_none))
        self.assertEqual(True, _test_file(path_file))
        self.assertEqual(False, _test_file(path_file_none))
        self.assertEqual(True, _test_file(path_template))
        self.assertEqual(False, _test_file(path_template_none))

        self.assertEqual(False, _test_link(path_content))
        self.assertEqual(False, _test_link(path_content_none))
        self.assertEqual(False, _test_link(path_file))
        self.assertEqual(False, _test_link(path_file_none))
        self.assertEqual(False, _test_link(path_template))
        self.assertEqual(False, _test_link(path_template_none))

        self.assertEqual(False, _test_directory(path_content))
        self.assertEqual(True, _test_directory(path_content_none))
        self.assertEqual(False, _test_directory(path_file))
        self.assertEqual(True, _test_directory(path_file_none))
        self.assertEqual(False, _test_directory(path_template))
        self.assertEqual(True, _test_directory(path_template_none))

    def test_implicit_link(self):
        path_src = {'path': 'path', 'src': 'src'}
        path_src_none = {'path': 'path', 'src': None}

        self.assertEqual(False, _test_file(path_src))
        self.assertEqual(False, _test_file(path_src_none))

        self.assertEqual(True, _test_link(path_src))
        self.assertEqual(False, _test_link(path_src_none))

        self.assertEqual(False, _test_directory(path_src))
        self.assertEqual(True, _test_directory(path_src_none))

    def test_implicit_directory(self):
        path = {'path': 'path'}

        self.assertEqual(False, _test_file(path))

        self.assertEqual(False, _test_link(path))

        self.assertEqual(True, _test_directory(path))
