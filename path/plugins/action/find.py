from __future__ import annotations

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
import os.path

display = Display()


class ActionModule(ActionBase):
    '''Return a list of paths based on specific criteria'''

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)

        validation, args = self.validate_argument_spec(
            argument_spec={
                'path': {'type': 'path', 'required': True},
                'patterns': {'type': 'list', 'default': [], 'elements': 'str'},
                'excludes': {'type': 'list', 'elements': 'str'},
                'relative': {'type': 'bool', 'default': False},
            },
        )

        display.v(f"Use 'ansible.builtin.find' to find paths in '{args['path']}'.")
        find = self._execute_module(
            module_name='ansible.builtin.find',
            module_args={
                'paths': [args['path']],
                'file_type': 'any',
                'hidden': True,
                'patterns': args['patterns'],
                'excludes': args['excludes'],
            },
            task_vars=task_vars,
        )

        files = find.pop('files')

        result.update(find)
        result['paths'] = []

        for file in files:
            path = file['path']
            if args['relative']:
                path = os.path.relpath(path, args['path'])
            if file['isreg']:
                result['paths'].append({
                    'path': path,
                    'state': 'file',
                    'user': file['pw_name'],
                    'group': file['gr_name'],
                    'mode': file['mode'],
                })
            elif file['isdir']:
                result['paths'].append({
                    'path': path,
                    'state': 'directory',
                    'user': file['pw_name'],
                    'group': file['gr_name'],
                    'mode': file['mode'],
                })
            elif file['islnk']:
                display.v(f"Use 'ansible.builtin.stat' to get '{file['path']}' stat.")
                stat = self._execute_module(
                    module_name='ansible.builtin.stat',
                    module_args={
                        'path': file['path'],
                    },
                    task_vars=task_vars,
                )
                if stat.get('failed', False):
                    return stat

                result['paths'].append({
                    'path': path,
                    'state': 'link',
                    'src': stat['stat']['lnk_target'],
                    'user': file['pw_name'],
                    'group': file['gr_name'],
                })

        return result
