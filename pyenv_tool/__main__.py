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
    pyenv_install,
    pyenv_installed_versions,
    pyenv_is_installed,
    pyenv_set_shims,
    pyenv_uninstall,
)
from pyenv_tool.python import VersionStatus, python_supported_versions


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
    "--no-update",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Do not update the pyenv tool or the list of available versions",
)
@click.option(
    "--dry-run",
    "-n",
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
    supported_status = dict(python_supported_versions())
    supported_versions = set(supported_status.keys())

    available_versions = {
        v for v in pyenv_available_versions() if v.prerelease == "" and v.build == ""
    }
    installed_versions = set(pyenv_installed_versions())

    deltas = list(
        calculate_changes(
            supported_versions,
            available_versions,
            installed_versions,
            keep_bugfix=keep_bugfix,
            remove_minor=remove_minor,
        ),
    )

    print()
    rprint("Version Report:")
    main_versions = set(supported_versions) | {v.main for v in installed_versions}

    for m in sorted(main_versions):
        s = supported_status.get(m, VersionStatus.UNSUPPORTED)

        rprint(
            f"  [bold]Python {m.main_format()} "
            f"([{s.value}]{s.value}[/{s.value}])[/bold]",
        )

        installed = {v for v in installed_versions if v.main == m}
        latest = max(v for v in available_versions if v.main == m)

        for v in sorted(installed):
            if s is VersionStatus.UNSUPPORTED:
                if v == latest:
                    rprint(
                        f"    {v} (installed, [ver_u]unsupported[/ver_u], [ver_l]latest[/ver_l])",
                    )
                else:
                    rprint(
                        f"    {v} (installed, [ver_u]unsupported[/ver_u])",
                    )

                if latest not in installed:
                    rprint(
                        f"    {latest} ([ver_u]unsupported[/ver_u], [ver_l]latest[/ver_l])",
                    )

            else:
                if v == latest:
                    rprint(f"    {v} (installed, [ver_l]latest[/ver_l])")
                else:
                    rprint(f"    {v} (installed, [ver_b]out-of-date[/ver_b])")

                if latest not in installed:
                    rprint(f"    {latest} ([ver_l]latest[/ver_l])")

        print()

    if len(deltas) <= 0:
        rprint("No changes required.")
        return 0

    for ver, op in sorted(deltas, reverse=True):
        if op is Op.INSTALL:
            rprint(f"  + Install [install]{ver.fixed_width}[/install]")
        elif op is Op.REMOVE:
            rprint(f"  - Remove  [remove]{ver.fixed_width}[/remove]")
        else:
            raise ValueError(f"Unexpected Operation: {op!s}")

    if not dry_run:
        to_install = sorted(
            (ver for ver, op in deltas if op is Op.INSTALL),
            reverse=True,
        )
        to_remove = sorted(
            (ver for ver, op in deltas if op is Op.REMOVE),
            reverse=True,
        )

        for v in to_install:
            rprint(f"Installing {v!s}...")
            out = pyenv_install(v)
            logger.debug(out)
            break

        for v in to_remove:
            rprint(f"Removing {v!s}...")
            pyenv_uninstall(v)

        main_versions = {v.main for v in pyenv_installed_versions()}
        latest_versions = sorted(
            (
                max(v for v in installed_versions if v.main == main)
                for main in main_versions
            ),
            reverse=True,
        )

        pyenv_set_shims(*latest_versions)

    return 0


cli_main.add_command(cli_upgrade, name="upgrade")

if __name__ == "__main__":
    sys.exit(cli_main())
