from __future__ import annotations

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.vars import combine_vars
from ..filter.state import _state as _filter_state

display = Display()


class ActionModule(ActionBase):
    """Handle path"""

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)

        validation, args = self.validate_argument_spec(
            argument_spec={
                'path': {'type': 'path', 'required': True},
                'state': {'type': 'str', 'choices': ['present', 'absent', 'file', 'link', 'directory'], 'default': 'present'},
                'content': {'type': 'str'},
                'file': {'type': 'path'},
                'template': {'type': 'path'},
                'vars': {'type': 'dict', 'default': {}},
                'src': {'type': 'path'},
                'user': {'type': 'str'},
                'group': {'type': 'str'},
                'mode': {'type': 'raw'},
                'validate': {'type': 'str'},
            },
            mutually_exclusive=[
                ['content', 'file', 'template'],
            ],
            required_if=[
                ['state', 'link', ['src']],
            ],
        )

        path_state = _filter_state(args)
        match path_state:
            case 'absent':
                result.update(
                    self.run_absent(args, task_vars)
                )
            case 'file':
                if args['content'] is not None:
                    result.update(
                        self.run_file_content(args, task_vars)
                    )
                elif args['file'] is not None:
                    result.update(
                        self.run_file_file(args, task_vars)
                    )
                elif args['template'] is not None:
                    result.update(
                        self.run_file_template(args, task_vars)
                    )
                else:
                    result.update(
                        self.run_file(args, task_vars)
                    )
            case 'link':
                result.update(
                    self.run_link(args, task_vars)
                )
            case 'directory':
                result.update(
                    self.run_directory(args, task_vars)
                )

        return result

    def run_absent(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.file' to ensure '{args['path']}' is absent.")
        return self._execute_module(
            module_name='ansible.builtin.file',
            module_args={
                'path': args['path'],
                'state': args['state'],
            },
            task_vars=task_vars,
        )

    def run_file_content(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.copy' to ensure '{args['path']}' content.")
        task = self._task.copy()
        task.args = {
            'dest': args['path'],
            'content': args['content'],
            'owner': args['user'],
            'group': args['group'],
            'mode': args['mode'],
            'validate': args['validate'],
        }
        return self._shared_loader_obj.action_loader.get(
            'ansible.builtin.copy',
            task=task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        ).run(
            task_vars=combine_vars(task_vars, args['vars'])
        )

    def run_file_file(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.copy' to ensure '{args['path']}' file.")
        task = self._task.copy()
        task.args = {
            'dest': args['path'],
            'src': args['file'],
            'owner': args['user'],
            'group': args['group'],
            'mode': args['mode'],
            'validate': args['validate'],
        }
        return self._shared_loader_obj.action_loader.get(
            'ansible.builtin.copy',
            task=task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        ).run(
            task_vars=task_vars
        )

    def run_file_template(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.template' to ensure '{args['path']}' template.")
        task = self._task.copy()
        task.args = {
            'src': args['template'],
            'dest': args['path'],
            'owner': args['user'],
            'group': args['group'],
            'mode': args['mode'],
            'validate': args['validate'],
        }
        return self._shared_loader_obj.action_loader.get(
            'ansible.builtin.template',
            task=task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        ).run(
            task_vars=combine_vars(task_vars, args['vars'])
        )

    def run_file(self, args, task_vars):
        remote_stat = self._execute_remote_stat(
            args['path'],
            all_vars=task_vars,
            follow=False,
            checksum=False,
        )

        file_state = 'touch'
        if remote_stat['exists']:
            file_state = 'file'

        display.v(f"Use 'ansible.builtin.file' to ensure '{args['path']}' state.")
        return self._execute_module(
            module_name='ansible.builtin.file',
            module_args={
                'path': args['path'],
                'state': file_state,
                'owner': args['user'],
                'group': args['group'],
                'mode': args['mode'],
            },
            task_vars=task_vars,
        )

    def run_link(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.file' to ensure '{args['path']}' is a link.")
        return self._execute_module(
            module_name='ansible.builtin.file',
            module_args={
                'path': args['path'],
                'src': args['src'],
                'state': 'link',
                'owner': args['user'],
                'group': args['group'],
            },
            task_vars=task_vars,
        )

    def run_directory(self, args, task_vars):
        display.v(f"Use 'ansible.builtin.file' to ensure '{args['path']}' is a directory.")
        return self._execute_module(
            module_name='ansible.builtin.file',
            module_args={
                'path': args['path'],
                'state': 'directory',
                'owner': args['user'],
                'group': args['group'],
                'mode': args['mode'],
            },
            task_vars=task_vars,
        )
