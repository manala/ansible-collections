from __future__ import annotations

from ansible.errors import AnsibleTemplateError


def _extension(paths, extension):
    if isinstance(paths, list):
        return [_do_extension(path, extension) for path in paths]

    return _do_extension(paths, extension)


def _do_extension(path, extension):
    if not isinstance(path, dict):
        raise AnsibleTemplateError(f'extension input expects a dict but was given a {type(path).__name__}')

    if not isinstance(extension, str):
        raise AnsibleTemplateError(f'extension option expects a string but was given a {type(extension).__name__}')

    if not extension.startswith('.'):
        extension = '.' + extension

    if not path['path'].endswith(extension):
        path['path'] += extension

    return path


class FilterModule(object):
    """ Manala path extension jinja2 filters """

    def filters(self):
        return {
            'extension': _extension,
        }
