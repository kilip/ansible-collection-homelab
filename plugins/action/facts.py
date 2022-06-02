from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        module_return = self._execute_module(module_name='gather_facts',
                                             module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)

        ret = dict()
        ret['hello'] = 'world'
        return dict(ansible_facts=dict(ret))
