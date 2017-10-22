import os
import os.path

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    home = "/home/toto"
    ssh_file = os.path.join(home, '.ssh')
    id_rsa_file = os.path.join(ssh_file, 'id_rsa')
    getent_a = host.ansible("getent", "database=passwd")
    assert 'toto' in getent_a['ansible_facts']['getent_passwd']
    ssh_a = host.ansible('stat', 'path={}'.format(ssh_file))
    assert ssh_a['stat']['exists']
    assert not ssh_a['stat']['xgrp']
    assert not ssh_a['stat']['xoth']
    id_rsa_a = host.ansible('stat', 'path={}'.format(id_rsa_file))
    assert id_rsa_a['stat']['exists']
