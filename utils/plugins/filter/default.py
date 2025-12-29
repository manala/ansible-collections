from __future__ import annotations

from ansible.errors import AnsibleTemplateError


def _default(data, *defaults):
    if isinstance(data, list):
        return [_do_default(item, *defaults) for item in data]

    return _do_default(data, *defaults)


def _do_default(data, *defaults):
    if not isinstance(data, dict):
        raise AnsibleTemplateError(f'default input expects a dict but was given a {type(data).__name__}')

    result = {}

    for default in reversed(defaults):
        if not isinstance(default, dict):
            raise AnsibleTemplateError(f'default options expects dicts but was given a {type(default).__name__}')
        result.update(default)

    result.update(data)

    return result


class FilterModule(object):
    """ Manala utils default jinja2 filters """

    def filters(self):
        return {
            'default': _default,
        }
