# Copyright: (c) 2022, Anthonius Munthi <me@itstoni.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
module: facts
short_description: Gather homelab configuration
description: This module will gather your homelab configuration
author:
    - Anthonius Munthi (@kilip)
'''

EXAMPLES = r'''
# Pass in a message
- name: Gather olympus facts
  kilip.homelab.facts:
    config_file: config.yml
    project_dir: "{{ lookup('env', 'PWD') }}"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
ansible_facts:
    description: The original name param that was passed in.
    type: str
    returned: always
'''
