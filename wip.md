# Switch collections

Pour utiliser les collections, tout en ayant la possibilité de lancer
le playbook depuis le répertoire :

* Les rôles sont à plat dans le répertoire roles ; il n'ont plus de préfixe
* Les rôles sont mis en place dans le répertoire ansible_collections/powo/tools/roles
* On a les répertoires pour les plugins et playbooks
* On installe les dépendances dans des répertoires spécifiques puis on lance le playbook
  à partir du répertoire courant

```shell
# Installation des dépendances
ANSIBLE_COLLECTIONS_PATH=dependencies/collections/ \
  ANSIBLE_ROLES_PATH=dependencies/roles/ \
  ansible-galaxy install -r dependencies/requirements.yml

# Run du playbook
ANSIBLE_CONFIG=inventory/ansible.cfg ansible-playbook powo.tools.install --check --diff -K
```