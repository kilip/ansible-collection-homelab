from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display


ENV_PROJECT_DIR = 'HOMELAB_PROJECT_DIR'
ENV_CONFIG_DIR = 'HOMELAB_CONFIG_DIR'
display = Display()


class ActionModule(ActionBase):

    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super(ActionModule, self).__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self.facts = dict()
        self.config_dir = ""
        self.project_dir = ""
        self.config_file = ""

    def _setup_path(self):
        # project_dir = self._loader.get_basedir()
        project_dir = ""
        if os.environ.get(ENV_PROJECT_DIR) is not None:
            project_dir = os.environ.get(ENV_PROJECT_DIR)

        config_dir = project_dir + "/config"
        if os.environ.get(ENV_CONFIG_DIR) is not None:
            config_dir = os.environ.get(ENV_CONFIG_DIR)

        self.config_dir = config_dir
        self.project_dir = project_dir

        self.facts['homelab_project_dir'] = project_dir
        self.facts['homelab_config_dir'] = config_dir
        self.facts['homelab_config_file'] = config_dir + "/homelab.sops.yml"

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        module_return = self._execute_module(
            module_name='setup',
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp
        )
        self._setup_path()

        return dict(ansible_facts=self.facts)
