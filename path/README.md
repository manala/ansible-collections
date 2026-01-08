# Ansible Collection - manala.path

[![homepage][image]][url]

[image]: https://raw.githubusercontent.com/manala/resources/main/logo.svg
[url]: https://www.manala.io/ "manala.io"

**The flexible, robust, and web oriented toolbox for Ansible !**

## Install

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```shell
ansible-galaxy collection install manala.path
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: manala.path
```

## Usage

See the [examples](examples).

## Release notes

See the [changelog](https://github.com/manala/ansible-collections/blob/main/path/CHANGELOG.md).

## Contribute

Found a bug ? Please open an [issue](https://github.com/manala/ansible-collections/issues)

You can contact us [here](manala-io.slack.com)

Any kind of contribution is very welcome, you can submit pull requests [here](https://github.com/manala/ansible-collections/pulls)

This collection uses [ansible-lint](https://github.com/ansible-community/ansible-lint), and `ansible-test` for linting and testing roles.


Open a docker shell
```shell
make sh
```

Launch sanity tests over a specific file or not
```shell
ansible-test sanity --python 3.13
ansible-test sanity --python 3.13 plugins/action/foo.py
```

Launch units tests over a specific file or not
```shell
ansible-test units --venv --python 3.13
ansible-test units --venv --python 3.13 tests/unit/plugins/filter/test_foo.py
```

Launch integration tests over a specific target or not
```shell
ansible-test integration
ansible-test integration foo
ansible-test integration foo --tags bar
```

## Licensing

This collection is distributed under the MIT license.

See [LICENSE](LICENSE) to see the full text.

# Author information

Manala [**(https://www.manala.io/)**](https://www.manala.io/)
