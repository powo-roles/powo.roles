import itertools

from jinja2 import evalcontextfilter


DISTRIBUTION_SYNONYMS = [
    ['RedHat', 'CentOS'],
]


@evalcontextfilter
def distro(ctx, arg, hostvars):
    if not isinstance(arg, dict):
        raise Exception('%s is not a dict' % (arg,))
    ansible_distribution = hostvars['ansible_distribution']
    ansible_distributions = set([
        distro
            for distros in DISTRIBUTION_SYNONYMS
                if ansible_distribution in distros
            for distro in distros
    ])
    ansible_distributions.add(ansible_distribution)
    ansible_distribution_version = hostvars['ansible_distribution_version']
    ansible_distribution_major_version = \
        hostvars['ansible_distribution_major_version']
    ansible_os_family = hostvars['ansible_os_family']
    tries = itertools.chain(
        ['%s_%s' % (distribution, ansible_distribution_version)
            for distribution in ansible_distributions],
        ['%s_%s' % (ansible_distribution, ansible_distribution_major_version)
            for distribution in ansible_distributions],
        ['%s' % (ansible_distribution,)
            for distribution in ansible_distributions],
        ['%s' % (ansible_os_family,)],
        ['default']
    )
    for distro_string in tries:
        if distro_string in arg:
            return arg[distro_string]
    return None


class FilterModule(object):
    def filters(self):
        return {'distro': distro}
