from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from ..filter.state import _state as _filter_state


def _file(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"file expects a dict but was given a {type(path).__name__}")

    return _filter_state(path) == 'file'


def _link(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"link expects a dict but was given a {type(path).__name__}")

    return _filter_state(path) == 'link'


def _directory(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"directory expects a dict but was given a {type(path).__name__}")

    return _filter_state(path) == 'directory'


class TestModule(object):
    """ Manala path state jinja2 tests """

    def tests(self):
        return {
            'file': _file,
            'link': _link,
            'directory': _directory,
        }
