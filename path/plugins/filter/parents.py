from __future__ import annotations

import os.path


def _parents(paths):
    result = []

    indexes = set()

    for path in paths:
        norm = os.path.normpath(path['path'])

        parents = []
        current = norm
        while True:
            parent = os.path.dirname(current)
            if not parent or parent == current:
                break
            parents.append(parent)
            current = parent

        for parent in reversed(parents):
            if parent not in indexes:
                indexes.add(parent)
                result.append({'path': parent})

        result.append(path)

    return result


class FilterModule(object):
    """ Manala path parents jinja2 filters """

    def filters(self):
        return {
            "parents": _parents,
        }
