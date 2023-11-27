"""Convienience wrapper for common pyenv operations."""

__author__ = """Matthew Wyant"""
__email__ = "me@matthewwyant.com"
__copyright__ = "Copyright 2023, Matthew Wyant"
__credits__ = [__author__]
__license__ = "GPL-3.0-plus"
__version__ = "0.1.0"
__version_info__ = (0, 1, 0)
__maintainer__ = __author__
__status__ = "Prototype"

import logging
from typing import Iterable, Tuple

from pyenv_tool.pyenv import Op
from pyenv_tool.python import PyVer


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
