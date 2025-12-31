from __future__ import annotations

from ansible.errors import AnsibleTemplateError


def _label(data, keep=None, remove=None, mask=None):
    if not isinstance(data, dict):
        raise AnsibleTemplateError(f'label input expects a dict but was given a {type(data).__name__}')

    # Keep
    keep = keep or []
    if keep:
        label = {key: data[key] for key in keep if key in data}
    else:
        label = data

    # Mask
    mask = set(mask or [])
    for key in mask:
        if key in data:
            label[key] = '<masked>'

    # Remove
    remove = set(remove or [])
    for key in remove:
        label.pop(key, None)

    return label


class FilterModule(object):
    """ Manala utils label jinja2 filters """

    def filters(self):
        return {
            'label': _label,
        }
