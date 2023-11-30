# PyEnv Tool

A convienience wrapper for common pyenv operations.

This tool is designed for Python developers who primarily use pyenv to keep
a complete array of up-to-date Python executables installed. This tool should
be considered porcelain to pyenv's plumbing, but NOT as a complete interface
replacement. Many pyenv operations will still need to be perfomed via pyenv's
interface.

## Operational Goal

`pyenvtool` is built around the concept of a "main" version which is composed
of a major and minor version, but ignores any bugfix, prerelease, or build
information. That is, `3.11.0`, `3.11-dev`, and `3.11.2` are all the same
"main" version of `3.11`.

`pyenvtool` operates with the goal that any existing main version of Python
should be left on the system, but updated if possible, and any supported main
versions of Python should be installed if absent.

-   For every main version that is _supported_ and _not present_ on the system:

    -   The latest bugfix version is installed

-   For every main version that is _supported_ and _present_ on the system:

    -   The latest bugfix version is installed if not already present
    -   Bugfix versions _prior_ to the latest are uninstalled, unless the
        `--keep-bugfix` option is provided

-   For every main version that is _unsupported_ and _present_ on the system:
    -   The latest bugfix version is installed if not already present, unless the
        `--remove-minor` option is provided
    -   Bugfix versions _prior_ to the latest are uninstalled, unless the
        `--keep-bugfix` option is provided

## Usage

Complete help documentation can be found by running `pyenvtool --help`, the
following is only a quick-start introduction.

The primary usage will be the `pyenvtool upgrade` command, which will perform
whatever pyenv operations are required to leave the system with a complete
array of up-to-date Python executables. By default, this command will:

-   Scrape python.org to determine which Python versions are currently supported
-   Update pyenv with the latest list of available versions (and possibly also
    update the pyenv tool itself).
-   Update any installed Python versions to the latest bugfix version (by
    installing the new version and uninstalling any old versions)
-   Install any supported Python versions, at the latest bugfix, which are not
    currently installed
-   Uninstall any unsupported Python versions EXCEPT for the latest bugfix

This behavior can be changed with the following command arguments:

`--keep-bugfix/-k`
Keep any existing python versions even if a newer bugfix is available.

`--remove-minor/-r`
Remove ALL unsupported python versions, including the latest bugfix.

`--no-update`
Do not update the pyenv tool or the list of available versions

`--dry-run/-n`
Check the system and determine the necessary changes, but do not execute
them.

## Installation

To install `pyenvtool`, run the following command. `python3` should point to
whatever Python binary you want to install it under, version 3.8 or later.

    python3 -m pip install git+https://github.com/therealzanfar/pyenvtool.git

### Prerequisites

This tool requires `pyenv` to be installed and available in the path. The
`pyenv` project can be found at https://github.com/pyenv/pyenv along with
documentation and installation instructions.

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[zanfar/cookiecutter-pypackage](https://gitlab.com/zanfar/cookiecutter-pypackage)
project template.
