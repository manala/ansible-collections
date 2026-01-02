from __future__ import annotations

from ansible.errors import AnsibleTemplateError
import fnmatch


def _match(path, pattern):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f'match expects a dict but was given a {type(path).__name__}')

    if pattern is None:
        return True

    return fnmatch.fnmatch(path['path'], pattern)


class TestModule(object):
    """ Manala path match jinja2 tests """

    def tests(self):
        return {
            'match': _match,
        }
