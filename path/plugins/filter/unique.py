from __future__ import annotations

from ansible.errors import AnsibleTemplateError
import os.path


def _unique(paths, pick='last', place='first'):

    if pick not in ('first', 'last'):
        raise AnsibleTemplateError(f"unique pick parameter must be 'first' or 'last', was given '{pick}'")
    if place not in ('first', 'last'):
        raise AnsibleTemplateError(f"unique place parameter must be 'first' or 'last', was given '{pick}'")

    indexes = {}

    for index, path in enumerate(paths):
        norm = os.path.normpath(path['path'])
        if norm not in indexes:
            indexes[norm] = {
                'first': index,
                'last': index,
            }
        else:
            indexes[norm]['last'] = index

    result = {}

    pick_first = (pick == 'first')
    place_first = (place == 'first')

    for value in indexes.values():
        path = paths[value['first']] if pick_first else paths[value['last']]
        index = value['first'] if place_first else value['last']
        result[index] = path

    return [result[i] for i in sorted(result)]


class FilterModule(object):
    """ Manala path unique jinja2 filters """

    def filters(self):
        return {
            "unique": _unique,
        }
