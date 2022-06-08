from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import yaml
from os.path import exists
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible_collections.community.sops.plugins.module_utils.sops import Sops

ENV_PROJECT_DIR = 'HOMELAB_PROJECT_DIR'
ENV_CONFIG_DIR = 'HOMELAB_CONFIG_DIR'
ENV_DEPLOY = 'HOMELAB_DEPLOY'
display = Display()


class ActionModule(ActionBase):

    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super(ActionModule, self).__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self.facts = dict()
        self.config_dir = ""
        self.project_dir = ""
        self.config_file = ""
        self.deploy = ""
        self.multi_env = False

    def _load_config(self, file):
        if not exists(file):
            return 0

        sops = Sops()
        content = sops.decrypt(encrypted_file=file, display=display)
        configs = yaml.safe_load(content)
        for key, value in configs.items():
            self.facts[key] = value

    def _configure_groups(self):
        groups = []
        for host in self.facts['homelab_hosts']:
            for group in host['groups']:
                if group not in groups:
                    groups.append(group)

        self.facts['homelab_groups'] = groups

    def _setup_path(self):
        # project_dir = self._loader.get_basedir()
        project_dir = ""
        if os.environ.get(ENV_PROJECT_DIR) is not None:
            project_dir = os.environ.get(ENV_PROJECT_DIR)

        config_dir = project_dir + "/config"
        if os.environ.get(ENV_CONFIG_DIR) is not None:
            config_dir = os.environ.get(ENV_CONFIG_DIR)

        inventory_dir = project_dir + "/ansible/inventory"
        if os.environ.get(ENV_DEPLOY) is not None:
            inventory_dir = inventory_dir + "/" + os.environ.get(ENV_DEPLOY)

        cluster_dir = project_dir + "/cluster"
        deploy_dir = cluster_dir + "/base/flux-system"
        if os.environ.get(ENV_DEPLOY) is not None:
            self.deploy = os.environ.get(ENV_DEPLOY)

        if self.deploy is not None:
            deploy_dir = cluster_dir + "/deploy/" + self.deploy

        self.config_dir = config_dir
        self.project_dir = project_dir
        self.config_file = config_dir + "/homelab.sops.yml"

        self._load_config(self.config_file)
        if self.deploy != "":
            deploy_config = self.config_dir + "/homelab." + self.deploy + ".sops.yml"
            self._load_config(deploy_config)
            inventory_dir = inventory_dir + "/" + self.deploy

        self.facts['homelab_deploy'] = self.deploy
        self.facts['homelab_project_dir'] = project_dir
        self.facts['homelab_inventory_dir'] = inventory_dir
        self.facts['homelab_config_dir'] = config_dir
        self.facts['homelab_config_file'] = self.config_file
        self.facts['homelab_cluster_dir'] = cluster_dir
        self.facts['homelab_deploy_dir'] = deploy_dir

        if "homelab_hosts" in self.facts:
            self._configure_groups()

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        module_return = self._execute_module(
            module_name='setup',
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp
        )
        # ansible_facts = module_return['ansible_facts']
        for key, value in task_vars.items():
            if key == 'homelab_deploy':
                self.deploy = value
            if key == 'homelab_multi_env':
                self.multi_env = value

        self._setup_path()

        return dict(ansible_facts=self.facts)
