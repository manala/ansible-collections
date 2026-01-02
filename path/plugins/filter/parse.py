from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from pathlib import Path


def _parse(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f'parse input expects a dict but was given a {type(path).__name__}')

    p = Path(path['path'])

    # Parent
    parent = str(p.parent)
    if parent in ['.', '/']:
        parent = ''

    # Extension
    extension = p.suffix.lstrip('.')

    return {
        'parent': parent,
        'name': p.name,
        'stem': p.stem,
        'extension': extension,
    }


class FilterModule(object):
    """ Manala path parse jinja2 filters """

    def filters(self):
        return {
            'parse': _parse,
        }
