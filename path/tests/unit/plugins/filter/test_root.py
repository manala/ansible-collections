from __future__ import annotations

import unittest
from plugins.filter.root import _root as _filter_root

from ansible.errors import AnsibleTemplateError


class TestRoot(unittest.TestCase):

    def test_invalid_input(self):
        paths = NotImplemented
        root_paths = {}

        with self.assertRaisesRegex(AnsibleTemplateError, f'root input expects a dict but was given a {type(paths).__name__}'):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f'root input expects a dict but was given a {type(paths).__name__}'):
            _filter_root([paths], root_paths)

    def test_invalid_root_paths(self):
        paths = {}
        root_paths = NotImplemented

        with self.assertRaisesRegex(AnsibleTemplateError, f'root options expects a dict or a string but was given a {type(root_paths).__name__}'):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f'root options expects a dict or a string but was given a {type(root_paths).__name__}'):
            _filter_root([paths], root_paths)

    def test_rooted_same_as_root(self):
        root_paths = '/foo'

        paths = {'path': '.'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/.' is the same as the root path '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/.' is the same as the root path '{root_paths}'"):
            _filter_root([paths], root_paths)

        paths = {'path': '../foo'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/../foo' is the same as the root path '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/../foo' is the same as the root path '{root_paths}'"):
            _filter_root([paths], root_paths)

        paths = {'path': 'bar/..'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/bar/..' is the same as the root path '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path '/foo/bar/..' is the same as the root path '{root_paths}'"):
            _filter_root([paths], root_paths)

    def test_traversal(self):
        root_paths = '/foo'

        paths = {'path': '/bar'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/bar' and root '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/bar' and root '{root_paths}'"):
            _filter_root([paths], root_paths)

        paths = {'path': '../bar'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/foo/../bar' and root '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/foo/../bar' and root '{root_paths}'"):
            _filter_root([paths], root_paths)

        paths = {'path': 'bar/../../baz'}

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/foo/bar/../../baz' and root '{root_paths}'"):
            _filter_root(paths, root_paths)

        with self.assertRaisesRegex(AnsibleTemplateError, f"path traversal between '/foo/bar/../../baz' and root '{root_paths}'"):
            _filter_root([paths], root_paths)

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

    def test_single_string(self):
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

    def test_multiple_mixed(self):
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
