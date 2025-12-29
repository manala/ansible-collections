from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from .state import _state as _filter_state


def _label(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"label input expects a dict but was given a {type(path).__name__}")

    if 'path' not in path:
        raise AnsibleTemplateError("label input expects a 'path' property")

    label = {
        'path': path['path'],
        'state': _filter_state(path),
    }

    match label['state']:
        case 'file':
            if path.get('content') is not None:
                label.update({
                    key: path[key] for key in ['user', 'group', 'mode'] if key in path
                })
            elif path.get('file') is not None:
                label.update({
                    key: path[key] for key in ['file', 'user', 'group', 'mode'] if key in path
                })
            elif path.get('template') is not None:
                label.update({
                    key: path[key] for key in ['template', 'user', 'group', 'mode'] if key in path
                })
            else:
                label.update({
                    key: path[key] for key in ['user', 'group', 'mode'] if key in path
                })
        case 'link':
            label.update({
                key: path[key] for key in ['src', 'user', 'group'] if key in path
            })
        case 'directory':
            label.update({
                key: path[key] for key in ['user', 'group', 'mode'] if key in path
            })

    return label


class FilterModule(object):
    """ Manala path label jinja2 filters """

    def filters(self):
        return {
            'label': _label,
        }
