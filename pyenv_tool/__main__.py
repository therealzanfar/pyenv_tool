#! /usr/bin/env python3

"""Console Entry Point for pyenv_tool Utility."""

import logging
import sys

import click

from pyenv_tool import calculate_changes
from pyenv_tool.cli import CLICK_CONTEXT, rprint, setup_logging
from pyenv_tool.pyenv import (  # , pyenv_update
    PYENV_NAME,
    Op,
    pyenv_available_versions,
    pyenv_installed_versions,
    pyenv_is_installed,
)
from pyenv_tool.python import python_supported_versions


@click.group(context_settings=CLICK_CONTEXT)
@click.option("-v", "--verbose", count=True)
def cli_main(verbose: int = 0) -> int:
    """Convienience wrapper for common pyenv operations."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    if not pyenv_is_installed():
        raise click.UsageError(
            f"Could not find pyenv executable `{PYENV_NAME}` "
            "or pyenv is not installed.",
        )

    return 0


@click.command(context_settings=CLICK_CONTEXT)
@click.option(
    "--keep-bugfix",
    "-k",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Keep all existing python versions even if a newer bugfix is available.",
)
@click.option(
    "--remove-minor",
    "-r",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Remove all unsupported python versions, including the latest bugfix.",
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Determine the necessary changes, but do not execute them.",
)
@click.option("-v", "--verbose", count=True)
def cli_upgrade(
    keep_bugfix: bool = False,
    remove_minor: bool = False,
    dry_run: bool = False,
    no_update: bool = False,
    verbose: int = 0,
) -> int:
    """Upgrade installed Python versions."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    if not no_update:
        rprint("Updating pyenv...")
        # pyenv_update()

    rprint("Scraping supported Python versions...")
    supported_versions = list(python_supported_versions())

    available_versions = list(pyenv_available_versions())
    installed_versions = list(pyenv_installed_versions())

    deltas = list(
        calculate_changes(
            supported_versions,
            available_versions,
            installed_versions,
            keep_bugfix=keep_bugfix,
            remove_minor=remove_minor,
        ),
    )

    if dry_run:
        rprint("Planned Changes:")
        for ver, op in sorted(deltas, reverse=True):
            if op is Op.INSTALL:
                rprint(f"  + Install [install]{ver.fixed_width}[/install]")
            elif op is Op.REMOVE:
                rprint(f"  - Remove  [remove]{ver.fixed_width}[/remove]")
            else:
                raise ValueError(f"Unexpected Operation: {op!s}")

    return 0


cli_main.add_command(cli_upgrade, name="upgrade")

if __name__ == "__main__":
    sys.exit(cli_main())
