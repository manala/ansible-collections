from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from .state import _state as _filter_state
from ..test.state import _file as _test_file
from ..test.state import _link as _test_link
from ..test.state import _directory as _test_directory
from ansible_collections.manala.utils.plugins.filter.default import _do_default as _utils_filter_do_default


def _default(paths, *default_paths, state=None):
    if isinstance(paths, list):
        return [_do_default(path, *default_paths, state=state) for path in paths]

    return _do_default(paths, *default_paths, state=state)


def _do_default(path, *default_paths, state=None):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f'default input expects a dict but was given a {type(path).__name__}')

    # Filter on state
    if state and _filter_state(path) != state:
        return path

    return _utils_filter_do_default(path, *default_paths)


class FilterModule(object):
    """ Manala path default jinja2 filters """

    def filters(self):
        return {
            'default': _default,
        }
