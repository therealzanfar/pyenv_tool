"""Convienience wrapper for common pyenv operations."""

__author__ = """Matthew Wyant"""
__email__ = "me@matthewwyant.com"
__copyright__ = "Copyright 2023, Matthew Wyant"
__credits__ = [__author__]
__license__ = "GPL-3.0-or-later"
__version__ = "1.0.0"
__version_info__ = (0, 1, 3)
__maintainer__ = __author__
__status__ = "Production"

import logging
from typing import Dict, Iterable, Tuple

from pyenvtool.cli import rprint
from pyenvtool.pyenv import Op
from pyenvtool.python import PyVer, VersionStatus


def calculate_changes(  # noqa: C901
    supported_versions: Iterable[PyVer],
    available_versions: Iterable[PyVer],
    installed_versions: Iterable[PyVer],
    keep_bugfix: bool = False,
    remove_minor: bool = False,
) -> Iterable[Tuple[PyVer, Op]]:
    """Calculate what changes need to be made."""
    logger = logging.getLogger(__name__)

    available_versions = [
        a for a in available_versions if a.prerelease == "" and a.build == ""
    ]

    main_sup = {s.main for s in supported_versions}
    main_old = {i.main for i in installed_versions if i.main not in main_sup}

    for s in main_sup:
        latest = None
        avail = [v for v in available_versions if v.main == s]
        installed = sorted(
            (v for v in installed_versions if v.main == s),
            reverse=True,
        )

        if len(avail) > 0:
            latest = max(avail)

            if latest not in installed:
                logger.debug(
                    f"Latest   {latest.major}.{latest.minor:02d} bugfix ({latest!s}) "
                    "needs to be installed.",
                )
                yield (latest, Op.INSTALL)

        if not keep_bugfix:
            for v in installed:
                if latest is not None and v != latest:
                    logger.debug(
                        f"Outdated {v.major}.{v.minor:02d} bugfix "
                        f"({v!s}) needs to be removed.",
                    )
                    yield (v, Op.REMOVE)

    for o in main_old:
        installed = sorted(
            (v for v in installed_versions if v.main == o),
            reverse=True,
        )

        if len(installed) > 0:
            latest = max(installed)

            for v in installed:
                if v == latest and remove_minor:
                    logger.debug(
                        f"Unsupported {v.major}.{v.minor:02d} minor "
                        f"({v!s}) needs to be removed.",
                    )
                    yield (v, Op.REMOVE)

                elif v != latest and not keep_bugfix:
                    logger.debug(
                        f"Unsupported {v.major}.{v.minor:02d} bugfix "
                        f"({v!s}) needs to be removed.",
                    )
                    yield (v, Op.REMOVE)


def print_version_report(
    supported_status: Dict[PyVer, VersionStatus],
    available_versions: Iterable[PyVer],
    installed_versions: Iterable[PyVer],
) -> None:
    """Pretty-print a report of the supported, installed, and available versions."""
    rprint("Version Report:")

    supported_versions = set(supported_status.keys())
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
                        f"    {v} (installed, [ver_u]unsupported[/ver_u],"
                        f" [ver_l]latest[/ver_l])",
                    )
                else:
                    rprint(
                        f"    {v} (installed, [ver_u]unsupported[/ver_u])",
                    )

                if latest not in installed:
                    rprint(
                        f"    {latest} ([ver_u]unsupported[/ver_u],"
                        f" [ver_l]latest[/ver_l])",
                    )

            else:
                if v == latest:
                    rprint(f"    {v} (installed, [ver_l]latest[/ver_l])")
                else:
                    rprint(f"    {v} (installed, [ver_b]out-of-date[/ver_b])")

                if latest not in installed:
                    rprint(f"    {latest} ([ver_l]latest[/ver_l])")

        print()
