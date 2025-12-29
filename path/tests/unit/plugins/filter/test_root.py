from __future__ import annotations

import unittest
from plugins.filter.root import _root as _filter_root

from ansible.errors import AnsibleTemplateError


class TestRoot(unittest.TestCase):

    def test_invalid_input(self):
        paths = NotImplemented
        root_paths = {}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual('root input expects a dict but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual('root input expects a dict but was given a NotImplementedType', str(error.exception))

    def test_invalid_root_paths(self):
        paths = {}
        root_paths = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual('root options expects a dict or a string but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual('root options expects a dict or a string but was given a NotImplementedType', str(error.exception))

    def test_rooted_same_as_root(self):
        root_paths = '/foo'

        paths = {'path': '.'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path '/foo/.' is the same as the root path '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path '/foo/.' is the same as the root path '/foo'", str(error.exception))

        paths = {'path': '../foo'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path '/foo/../foo' is the same as the root path '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path '/foo/../foo' is the same as the root path '/foo'", str(error.exception))

        paths = {'path': 'bar/..'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path '/foo/bar/..' is the same as the root path '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path '/foo/bar/..' is the same as the root path '/foo'", str(error.exception))

    def test_traversal(self):
        root_paths = '/foo'

        paths = {'path': '/bar'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path traversal between '/bar' and root '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path traversal between '/bar' and root '/foo'", str(error.exception))

        paths = {'path': '../bar'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path traversal between '/foo/../bar' and root '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path traversal between '/foo/../bar' and root '/foo'", str(error.exception))

        paths = {'path': 'bar/../../baz'}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root(paths, root_paths)
        self.assertEqual("path traversal between '/foo/bar/../../baz' and root '/foo'", str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_root([paths], root_paths)
        self.assertEqual("path traversal between '/foo/bar/../../baz' and root '/foo'", str(error.exception))

    def test_single_dict(self):
        self.assertEqual({
            'path': '/foo/bar',
        }, _filter_root(
            {'path': 'bar'},
            {'path': '/foo'},
        ))
        self.assertEqual([
            {'path': '/foo/bar'},
            {'path': '/foo/baz'},
            {'path': '/foo/bar/baz'},
        ], _filter_root([
            {'path': 'bar'},
            {'path': 'baz'},
            {'path': 'bar/baz'},
        ],
            {'path': '/foo'},
        ))

    def test_option_single_string(self):
        self.assertEqual({
            'path': '/foo/bar',
        }, _filter_root(
            {'path': 'bar'},
            '/foo',
        ))
        self.assertEqual([
            {'path': '/foo/bar'},
            {'path': '/foo/baz'},
            {'path': '/foo/bar/baz'},
        ], _filter_root([
            {'path': 'bar'},
            {'path': 'baz'},
            {'path': 'bar/baz'},
        ],
            '/foo',
        ))

    def test_options_multiple_mixed(self):
        self.assertEqual({
            'path': '/foo/bar/baz',
        }, _filter_root(
            {'path': 'baz'},
            {'path': '/foo'}, 'bar',
        ))
        self.assertEqual([
            {'path': '/foo/bar/baz'},
            {'path': '/foo/bar/qux'},
            {'path': '/foo/bar/baz/qux'},
        ], _filter_root([
            {'path': 'baz'},
            {'path': 'qux'},
            {'path': 'baz/qux'},
        ],
            {'path': '/foo'}, 'bar',
        ))
