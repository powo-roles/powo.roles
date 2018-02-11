import os
import os.path

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    setup = host.ansible("setup")["ansible_facts"]
    pkgs = host.ansible(setup["ansible_pkg_mgr"],
                        "list=installed")
    assert len([i for i in pkgs['results']
                if i['name'] == 'rpmfusion-free-release']) == 1
    assert len([i for i in pkgs['results']
                if i['name'] == 'rpmfusion-nonfree-release']) == 1
