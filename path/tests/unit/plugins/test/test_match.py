from __future__ import annotations

import unittest
from plugins.test.match import _match as _test_match

from ansible.errors import AnsibleTemplateError


class TestMatch(unittest.TestCase):

    def test_invalid_input(self):
        path = NotImplemented

        with self.assertRaises(AnsibleTemplateError) as error:
            _test_match(path, None)
        self.assertEqual('match expects a dict but was given a NotImplementedType', str(error.exception))

    def test_none_pattern(self):
        pattern = None

        self.assertEqual(True, _test_match({'path': '/foo'}, pattern))
        self.assertEqual(True, _test_match({'path': '/foo/bar'}, pattern))
        self.assertEqual(True, _test_match({'path': '/foo/baz'}, pattern))

    def test_empty_pattern(self):
        pattern = ''

        self.assertEqual(False, _test_match({'path': '/foo'}, pattern))
        self.assertEqual(False, _test_match({'path': '/foo/bar'}, pattern))
        self.assertEqual(False, _test_match({'path': '/foo/baz'}, pattern))

    def test(self):
        path = {'path': '/foo'}
        self.assertEqual(True, _test_match(path, '/foo'))
        self.assertEqual(False, _test_match(path, 'foo'))
        self.assertEqual(False, _test_match(path, '/bar'))
        self.assertEqual(True, _test_match(path, '/*'))
        self.assertEqual(True, _test_match(path, '*'))
        self.assertEqual(True, _test_match(path, '/foo*'))
        self.assertEqual(False, _test_match(path, 'foo*'))
        self.assertEqual(True, _test_match(path, '*foo'))
        self.assertEqual(False, _test_match(path, '*bar'))
        self.assertEqual(True, _test_match(path, '*foo*'))
        self.assertEqual(False, _test_match(path, '*bar*'))
        self.assertEqual(True, _test_match(path, '*f*'))
        self.assertEqual(False, _test_match(path, '*b*'))

        path = {'path': '/foo/bar'}
        self.assertEqual(True, _test_match(path, '/foo/bar'))
        self.assertEqual(False, _test_match(path, 'foo'))
        self.assertEqual(False, _test_match(path, 'foo/bar'))
        self.assertEqual(False, _test_match(path, '/bar/baz'))
        self.assertEqual(True, _test_match(path, '/*/*'))
        self.assertEqual(True, _test_match(path, '/*'))
        self.assertEqual(True, _test_match(path, '*/*'))
        self.assertEqual(True, _test_match(path, '*'))
        self.assertEqual(True, _test_match(path, '/foo/bar*'))
        self.assertEqual(True, _test_match(path, '/foo/*'))
        self.assertEqual(False, _test_match(path, 'foo/bar*'))
        self.assertEqual(False, _test_match(path, 'foo*'))
        self.assertEqual(True, _test_match(path, '*foo/bar'))
        self.assertEqual(False, _test_match(path, '*foo'))
        self.assertEqual(True, _test_match(path, '*bar'))
        self.assertEqual(True, _test_match(path, '*foo/bar*'))
        self.assertEqual(True, _test_match(path, '*foo*'))
        self.assertEqual(True, _test_match(path, '*bar*'))
        self.assertEqual(True, _test_match(path, '*f*'))
        self.assertEqual(True, _test_match(path, '*b*'))
