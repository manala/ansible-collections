from __future__ import annotations

from ansible.errors import AnsibleTemplateError
import os.path


def _root(paths, *root_paths):
    if isinstance(paths, list):
        return [_do_root(path, *root_paths) for path in paths]

    return _do_root(paths, *root_paths)


def _do_root(path, *root_paths):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f"root input expects a dict but was given a {type(path).__name__}")

    paths = []

    for root_path in root_paths:
        match root_path:
            case str():
                paths.append(root_path)
            case dict():
                paths.append(root_path['path'])
            case _:
                raise AnsibleTemplateError(f"root options expects a dict or a string but was given a {type(root_path).__name__}")

    root_path = os.path.join(*paths)
    root_norm_path = os.path.normpath(root_path)

    final_path = os.path.join(root_path, path['path'])
    final_norm_path = os.path.normpath(final_path)

    if final_norm_path == root_norm_path:
        raise AnsibleTemplateError(f"path '{final_path}' is the same as the root path '{root_path}'")

    if not final_norm_path.startswith(root_norm_path + os.sep):
        raise AnsibleTemplateError(f"path traversal between '{final_path}' and root '{root_path}'")

    path['path'] = final_path

    return path


class FilterModule(object):
    """ Manala path root jinja2 filters """

    def filters(self):
        return {
            'root': _root,
        }
