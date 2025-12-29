from __future__ import annotations

import unittest
from plugins.filter.default import _default as _filter_default

from ansible.errors import AnsibleTemplateError


class TestDefault(unittest.TestCase):

    def test_invalid_input(self):
        paths = NotImplemented
        default_paths = {}

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default(paths, {})
        self.assertEqual('default input expects a dict but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default([paths], {})
        self.assertEqual('default input expects a dict but was given a NotImplementedType', str(error.exception))

    def test_invalid_default_paths(self):
        paths = {'path': 'path'}
        default_paths = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default(paths, default_paths)
        self.assertEqual('default options expects dicts but was given a NotImplementedType', str(error.exception))

        with self.assertRaises(AnsibleTemplateError) as error:
            _filter_default([paths], default_paths)
        self.assertEqual('default options expects dicts but was given a NotImplementedType', str(error.exception))

    def test_file(self):
        default_paths = {'user': 'bar', 'group': 'group'}

        paths = {'path': 'path', 'state': 'file', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo', },
            _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            _filter_default(paths, default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths, state='directory'),
        )

    def test_file_multiple(self):
        default_paths = [
            {'user': 'bar', 'group': 'foo', 'mode': 'mode'},
            {'group': 'bar', 'validate': 'validate'},
        ]

        paths = {'path': 'path', 'state': 'file', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths, state='directory'),
        )

    def test_link(self):
        default_paths = {'user': 'bar', 'group': 'group'}

        paths = {'path': 'path', 'state': 'link', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            _filter_default(paths, default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths, state='directory'),
        )

    def test_link_multiple(self):
        default_paths = [
            {'user': 'bar', 'group': 'foo', 'mode': 'mode'},
            {'group': 'bar', 'validate': 'validate'},
        ]

        paths = {'path': 'path', 'state': 'link', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths, state='directory'),
        )

    def test_directory(self):
        default_paths = {'user': 'bar', 'group': 'group'}

        paths = {'path': 'path', 'state': 'directory', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
            _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
            _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
            _filter_default(paths, default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'group'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'group'},
        ], _filter_default(paths, default_paths, state='directory'),
        )

    def test_directory_multiple(self):
        default_paths = [
            {'user': 'bar', 'group': 'foo', 'mode': 'mode'},
            {'group': 'bar', 'validate': 'validate'},
        ]

        paths = {'path': 'path', 'state': 'directory', 'user': 'foo'}

        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
            _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual(
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            _filter_default(paths, *default_paths, state='directory'),
        )

        paths = [
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ]

        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='file'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
            {'path': 'path', 'state': 'directory', 'user': 'foo'},
        ], _filter_default(paths, *default_paths, state='link'),
        )
        self.assertEqual([
            {'path': 'path', 'state': 'file', 'user': 'foo'},
            {'path': 'path', 'state': 'link', 'user': 'foo'},
            {'path': 'path', 'state': 'directory', 'user': 'foo', 'group': 'foo', 'mode': 'mode', 'validate': 'validate'},
        ], _filter_default(paths, *default_paths, state='directory'),
        )
