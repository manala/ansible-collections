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

        self.assertTrue(_test_match({'path': '/foo'}, pattern))
        self.assertTrue(_test_match({'path': '/foo/bar'}, pattern))
        self.assertTrue(_test_match({'path': '/foo/baz'}, pattern))

    def test_empty_pattern(self):
        pattern = ''

        self.assertFalse(_test_match({'path': '/foo'}, pattern))
        self.assertFalse(_test_match({'path': '/foo/bar'}, pattern))
        self.assertFalse(_test_match({'path': '/foo/baz'}, pattern))

    def test(self):
        path = {'path': '/foo'}
        self.assertTrue(_test_match(path, '/foo'))
        self.assertFalse(_test_match(path, 'foo'))
        self.assertFalse(_test_match(path, '/bar'))
        self.assertTrue(_test_match(path, '/*'))
        self.assertTrue(_test_match(path, '*'))
        self.assertTrue(_test_match(path, '/foo*'))
        self.assertFalse(_test_match(path, 'foo*'))
        self.assertTrue(_test_match(path, '*foo'))
        self.assertFalse(_test_match(path, '*bar'))
        self.assertTrue(_test_match(path, '*foo*'))
        self.assertFalse(_test_match(path, '*bar*'))
        self.assertTrue(_test_match(path, '*f*'))
        self.assertFalse(_test_match(path, '*b*'))

        path = {'path': '/foo/bar'}
        self.assertTrue(_test_match(path, '/foo/bar'))
        self.assertFalse(_test_match(path, 'foo'))
        self.assertFalse(_test_match(path, 'foo/bar'))
        self.assertFalse(_test_match(path, '/bar/baz'))
        self.assertTrue(_test_match(path, '/*/*'))
        self.assertTrue(_test_match(path, '/*'))
        self.assertTrue(_test_match(path, '*/*'))
        self.assertTrue(_test_match(path, '*'))
        self.assertTrue(_test_match(path, '/foo/bar*'))
        self.assertTrue(_test_match(path, '/foo/*'))
        self.assertFalse(_test_match(path, 'foo/bar*'))
        self.assertFalse(_test_match(path, 'foo*'))
        self.assertTrue(_test_match(path, '*foo/bar'))
        self.assertFalse(_test_match(path, '*foo'))
        self.assertTrue(_test_match(path, '*bar'))
        self.assertTrue(_test_match(path, '*foo/bar*'))
        self.assertTrue(_test_match(path, '*foo*'))
        self.assertTrue(_test_match(path, '*bar*'))
        self.assertTrue(_test_match(path, '*f*'))
        self.assertTrue(_test_match(path, '*b*'))
