#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = r"""
---
module: ah_ee_registry_index
author: "Tom Page (@Tompage1994)"
short_description: Initiate an execution environment registry indexing.
description:
    - Initiate an execution environment registry indexing. See
      U(https://www.ansible.com/) for an overview.
options:
    name:
      description:
        - Registry name
      required: True
      type: str
    wait:
      description:
        - Wait for the registry to finish indexing before returning.
      required: false
      default: True
      type: bool
    interval:
      description:
        - The interval to request an update from Automation Hub.
      required: False
      default: 1
      type: float
    timeout:
      description:
        - If waiting for the registry to index this will abort after this
          amount of seconds
      type: int
notes:
  - Only works when registry URL is registry.redhat.io
extends_documentation_fragment: ansible.automation_hub.auth_ui
"""


EXAMPLES = """
- name: Index redhat registry without waiting
  ansible.automation_hub.ah_ee_registry_index:
    name: redhat
    wait: false

- name: Index registry.redhat.io registry and wait up to 300 seconds
  ansible.automation_hub.ah_ee_registry_index:
    name: registry_redhat_io
    wait: true
    timeout: 300
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIEERegistry


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        wait=dict(default=True, type="bool"),
        interval=dict(default=1.0, type="float"),
        timeout=dict(default=None, type="int"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec)

    # Extract our parameters
    name = module.params.get("name")
    wait = module.params.get("wait")
    interval = module.params.get("interval")
    timeout = module.params.get("timeout")

    module.authenticate()
    vers = module.get_server_version()
    registry = AHUIEERegistry(module)
    if vers > "4.7.0":
        registry.id_field = "id"
    registry.get_object(name, vers)

    if not registry.exists:
        module.fail_json(msg="The registery with name: {name}, was not found.".format(name=name))

    registry.index(wait, interval, timeout)


if __name__ == "__main__":
    main()
