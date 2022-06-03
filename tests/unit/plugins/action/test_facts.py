from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
from ....unit.compat import unittest
from ....unit.compat.mock import MagicMock, patch
from ....unit.mock.loader import DictDataLoader

from ansible import constants as C
from ansible.playbook.task import Task
from ansible.template import Templar
from ansible.executor import module_common

from ansible_collections.kilip.homelab.plugins.action.facts import ActionModule as FactsAction
from ansible_collections.kilip.homelab.plugins.action.facts import ENV_PROJECT_DIR


class TestFacts(unittest.TestCase):
    task = MagicMock(Task)
    play_context = MagicMock()
    play_context.check_mode = False
    connection = MagicMock()
    fake_loader = DictDataLoader({
    })
    templar = Templar(loader=fake_loader)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_facts_default(self):
        os.environ[ENV_PROJECT_DIR] = "/tmp/homelab"
        self.task.action = 'kilip.homelab.facts'
        self.task.async_val = False
        self.task.args = {}

        plugin = FactsAction(
            self.task,
            self.connection,
            self.play_context,
            loader=None,
            templar=self.templar,
            shared_loader_obj=None
        )
        get_module_args = MagicMock()
        plugin._get_module_args = get_module_args
        plugin._execute_module = MagicMock

        result = plugin.run(dict())
        facts = result["ansible_facts"]

        # self.assertEqual(os.environ[ENV_PROJECT_DIR], "hello")
        self.assertEqual("/tmp/homelab", facts["homelab_project_dir"])
        self.assertEqual("/tmp/homelab/config", facts["homelab_config_dir"])
        self.assertEqual("/tmp/homelab/config/homelab.sops.yml", facts["homelab_config_file"])
