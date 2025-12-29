from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from .state import _state as _filter_state
from ..test.state import _file as _test_file
from ..test.state import _link as _test_link
from ..test.state import _directory as _test_directory


def _default(paths, *default_paths, state=None):
    if isinstance(paths, list):
        return [_do_default(path, *default_paths, state=state) for path in paths]

    return _do_default(paths, *default_paths, state=state)


def _do_default(path, *default_paths, state=None):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"default input expects a dict but was given a {type(path).__name__}")

    # Filter on state
    if state and _filter_state(path) != state:
        return path

    result = {}

    for default_path in reversed(default_paths):
        if not isinstance(default_path, dict):
            raise AnsibleTemplateError(f"default options expects dicts but was given a {type(default_path).__name__}")
        result.update(default_path)

    result.update(path)

    return result


def _default_file(paths, *default_paths):
    if isinstance(paths, list):
        return [_do_default_file(path, *default_paths) for path in paths]

    return _do_default_file(paths, *default_paths)


def _do_default_file(path, *default_paths):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"default_file input expects a dict but was given a {type(path).__name__}")

    if _test_file(path):
        return _default(path, *default_paths)

    return path


def _default_link(paths, *default_paths):
    if isinstance(paths, list):
        return [_do_default_link(path, *default_paths) for path in paths]

    return _do_default_link(paths, *default_paths)


def _do_default_link(path, *default_paths):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"default_link input expects a dict but was given a {type(path).__name__}")

    if _test_link(path):
        return _default(path, *default_paths)

    return path


def _default_directory(paths, *default_paths):
    if isinstance(paths, list):
        return [_do_default_directory(path, *default_paths) for path in paths]

    return _do_default_directory(paths, *default_paths)


def _do_default_directory(path, *default_paths):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"default_directory input expects a dict but was given a {type(path).__name__}")

    if _test_directory(path):
        return _default(path, *default_paths)

    return path


class FilterModule(object):
    """ Manala path default jinja2 filters """

    def filters(self):
        return {
            'default': _default,
            'default_file': _default_file,
            'default_link': _default_link,
            'default_directory': _default_directory,
        }
