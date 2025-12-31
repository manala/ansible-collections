from __future__ import annotations

from ansible.errors import AnsibleTemplateError
from .state import _state as _filter_state
from ansible_collections.manala.utils.plugins.filter.label import _label as _utils_filter_label


def _label(path):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"label input expects a dict but was given a {type(path).__name__}")

    if 'path' not in path:
        raise AnsibleTemplateError("label input expects a 'path' property")

    # Normalize path state
    path['state'] = _filter_state(path)

    match path['state']:
        case 'file':
            return _utils_filter_label(path, keep=['path', 'state', 'content', 'file', 'template', 'user', 'group', 'mode'], mask=['content'])
        case 'link':
            return _utils_filter_label(path, keep=['path', 'state', 'src', 'user', 'group'])
        case 'directory':
            return _utils_filter_label(path, keep=['path', 'state', 'user', 'group', 'mode'])
        case 'absent':
            return _utils_filter_label(path, keep=['path', 'state'])


class FilterModule(object):
    """ Manala path label jinja2 filters """

    def filters(self):
        return {
            'label': _label,
        }
