from __future__ import annotations

import os.path


def _exclusify(paths, against_paths):
    result = paths.copy()

    norm_paths = {os.path.normpath(path['path']) for path in paths}

    for against_path in against_paths:
        against_norm_path = os.path.normpath(against_path['path'])
        if against_norm_path not in norm_paths:
            against_path = {
                'path': against_path['path'],
                'state': 'absent',
            }
            result.append(against_path)

    return result


class FilterModule(object):
    """ Manala path exclusify jinja2 filters """

    def filters(self):
        return {
            "exclusify": _exclusify,
        }
