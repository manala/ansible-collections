from __future__ import annotations

import unittest
from plugins.test.state import _file as _test_file
from plugins.test.state import _link as _test_link
from plugins.test.state import _directory as _test_directory
from plugins.test.state import _present as _test_present
from plugins.test.state import _absent as _test_absent

from ansible.errors import AnsibleTemplateError


class TestFile(unittest.TestCase):

    def test_invalid_input(self):
        path = NotImplemented

        with self.assertRaisesRegex(AnsibleTemplateError, f'file expects a dict but was given a {type(path).__name__}'):
            _test_file(path)

        with self.assertRaisesRegex(AnsibleTemplateError, f'link expects a dict but was given a {type(path).__name__}'):
            _test_link(path)

        with self.assertRaisesRegex(AnsibleTemplateError, f'directory expects a dict but was given a {type(path).__name__}'):
            _test_directory(path)

    def test_empty(self):
        path = {}

        self.assertFalse(_test_file(path))
        self.assertFalse(_test_link(path))
        self.assertTrue(_test_directory(path))
        self.assertTrue(_test_present(path))
        self.assertFalse(_test_absent(path))

    def test_explicit(self):
        path_absent = {'path': 'path', 'state': 'absent'}
        path_file = {'path': 'path', 'state': 'file'}
        path_link = {'path': 'path', 'state': 'link'}
        path_directory = {'path': 'path', 'state': 'directory'}

        self.assertFalse(_test_file(path_absent))
        self.assertTrue(_test_file(path_file))
        self.assertFalse(_test_file(path_link))
        self.assertFalse(_test_file(path_directory))

        self.assertFalse(_test_link(path_absent))
        self.assertFalse(_test_link(path_file))
        self.assertTrue(_test_link(path_link))
        self.assertFalse(_test_link(path_directory))

        self.assertFalse(_test_directory(path_absent))
        self.assertFalse(_test_directory(path_file))
        self.assertFalse(_test_directory(path_link))
        self.assertTrue(_test_directory(path_directory))

        self.assertFalse(_test_present(path_absent))
        self.assertTrue(_test_present(path_file))
        self.assertTrue(_test_present(path_link))
        self.assertTrue(_test_present(path_directory))

        self.assertTrue(_test_absent(path_absent))
        self.assertFalse(_test_absent(path_file))
        self.assertFalse(_test_absent(path_link))
        self.assertFalse(_test_absent(path_directory))

    def test_implicit_file(self):
        path_content = {'path': 'path', 'content': 'content'}
        path_content_none = {'path': 'path', 'content': None}
        path_file = {'path': 'path', 'file': 'file'}
        path_file_none = {'path': 'path', 'file': None}
        path_template = {'path': 'path', 'template': 'template'}
        path_template_none = {'path': 'path', 'template': None}

        self.assertTrue(_test_file(path_content))
        self.assertFalse(_test_file(path_content_none))
        self.assertTrue(_test_file(path_file))
        self.assertFalse(_test_file(path_file_none))
        self.assertTrue(_test_file(path_template))
        self.assertFalse(_test_file(path_template_none))

        self.assertFalse(_test_link(path_content))
        self.assertFalse(_test_link(path_content_none))
        self.assertFalse(_test_link(path_file))
        self.assertFalse(_test_link(path_file_none))
        self.assertFalse(_test_link(path_template))
        self.assertFalse(_test_link(path_template_none))

        self.assertFalse(_test_directory(path_content))
        self.assertTrue(_test_directory(path_content_none))
        self.assertFalse(_test_directory(path_file))
        self.assertTrue(_test_directory(path_file_none))
        self.assertFalse(_test_directory(path_template))
        self.assertTrue(_test_directory(path_template_none))

        self.assertTrue(_test_present(path_content))
        self.assertTrue(_test_present(path_content_none))
        self.assertTrue(_test_present(path_file))
        self.assertTrue(_test_present(path_file_none))
        self.assertTrue(_test_present(path_template))
        self.assertTrue(_test_present(path_template_none))

        self.assertFalse(_test_absent(path_content))
        self.assertFalse(_test_absent(path_content_none))
        self.assertFalse(_test_absent(path_file))
        self.assertFalse(_test_absent(path_file_none))
        self.assertFalse(_test_absent(path_template))
        self.assertFalse(_test_absent(path_template_none))

    def test_implicit_link(self):
        path_src = {'path': 'path', 'src': 'src'}
        path_src_none = {'path': 'path', 'src': None}

        self.assertFalse(_test_file(path_src))
        self.assertFalse(_test_file(path_src_none))

        self.assertTrue(_test_link(path_src))
        self.assertFalse(_test_link(path_src_none))

        self.assertFalse(_test_directory(path_src))
        self.assertTrue(_test_directory(path_src_none))

        self.assertTrue(_test_present(path_src))
        self.assertTrue(_test_present(path_src_none))

        self.assertFalse(_test_absent(path_src))
        self.assertFalse(_test_absent(path_src_none))

    def test_implicit_directory(self):
        path = {'path': 'path'}

        self.assertFalse(_test_file(path))

        self.assertFalse(_test_link(path))

        self.assertTrue(_test_directory(path))

        self.assertTrue(_test_present(path))

        self.assertFalse(_test_absent(path))
