# PyEnv Tool

A convienience wrapper for common pyenv operations.

This tool is designed for Python developers who primarily use pyenv to keep
a complete array of up-to-date Python executables installed. This tool should
be considered porcelain to pyenv's plumbing, but NOT as a complete interface
replacement. Many pyenv operations will still need to be perfomed via pyenv's
interface.

## Usage

Complete help documentation can be found by running `pyenvtool --help`, the
following is only a quick-start introduction.

The primary usage will be the `pyenvtool upgrade` command, which will perform
whatever pyenv operations are required to leave the system with a complete
array of up-to-date Python executables. By default, this command will:

- Scrape python.org to determine which Python versions are currently supported
- Update pyenv with the latest list of available versions (and possibly also
    update the pyenv tool itself).
- Update any installed Python versions to the latest bugfix version (by
    installing the new version and uninstalling any old versions)
- Install any supported Python versions, at the latest bugfix, which are not
    currently installed
- Uninstall any unsupported Python versions EXCEPT for the latest bugfix

This behavior can be changed with the following command arguments:

`--keep-bugfix`
    Keep any existing python versions even if a newer bugfix is available.

`--remove-minor`
    Remove ALL unsupported python versions, including the latest bugfix.

`--no-update`
    Do not update the pyenv tool or the list of available versions

`--dry-run`
    Check the system and determine the necessary changes, but do not execute
    them.

## Installation

    python3 -m pip install git+https://github.com/therealzanfar/pyenv_tool.git

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[zanfar/cookiecutter-pypackage](https://gitlab.com/zanfar/cookiecutter-pypackage)
project template.
