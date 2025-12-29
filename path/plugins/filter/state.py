from __future__ import annotations

from ansible.errors import AnsibleTemplateError


def _state(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"state input expects a dict but was given a {type(path).__name__}")

    state = path.get('state', 'present')

    # Explicit
    if state in ['absent', 'file', 'link', 'directory']:
        return state

    # Implicit - File
    if any(path.get(key) is not None for key in ('content', 'file', 'template')):
        return 'file'

    # Implicit - Link
    if path.get('src') is not None:
        return 'link'

    # Implicit - Directory
    return 'directory'


class FilterModule(object):
    """ Manala path state jinja2 filters """

    def filters(self):
        return {
            'state': _state,
        }
