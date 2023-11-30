"""Methods and Objects for interacting with `pyenv`."""

import logging
import shutil
import subprocess
from enum import Enum, auto
from typing import Iterator

from pyenvtool.python import PyVer

PYENV_NAME = "pyenv"


class Op(int, Enum):
    """Possible PyEnv Operations."""

    INSTALL = auto()
    KEEP = auto()
    REMOVE = auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name})"


def pyenv_is_installed() -> bool:
    """Determine if pyenv is installed."""
    pyenv_path = shutil.which(PYENV_NAME)
    return pyenv_path is not None


def pyenv_execute(*args: str, dry_run: bool = False) -> str:
    """Execute pyenv with the provided arguments and return the output."""
    logger = logging.getLogger(__name__)
    logger.info("Executing: " + " ".join([PYENV_NAME, *args]))

    if dry_run:
        return ""

    ps = subprocess.run(
        [PYENV_NAME, *args],
        capture_output=True,
        check=True,
        text=True,
        encoding="utf-8",
    )

    return ps.stdout


def pyenv_update() -> None:
    """
    Update pyenv.

    Assumed to be sucessfull, raise an error if not.
    """
    pyenv_execute("update")


def pyenv_available_versions() -> Iterator[PyVer]:
    """Determine which python versions can be installed by pyenv."""
    logger = logging.getLogger(__name__)

    for line in pyenv_execute("install", "--list").splitlines():
        ident = line.strip()

        if ident[0] not in "0123456789":
            continue

        try:
            ver = PyVer.parse(ident)
        except ValueError as e:
            logger.warning(f"Unexpected invalid Python version: {ident} ({e!s})")
            continue

        logger.debug(f"Found available version {ver!s}")
        yield ver


def pyenv_installed_versions() -> Iterator[PyVer]:
    """Determine which python shims are currently installed."""
    logger = logging.getLogger(__name__)

    for line in pyenv_execute("versions").splitlines():
        parts = line.strip().split()

        ident = parts[0]
        if parts[0] == "*":
            ident = parts[1]

        if ident == "system":
            continue

        try:
            ver = PyVer.parse(ident)
        except ValueError as e:
            logger.warning(f"Unexpected invalid Python version: {ident} ({e!s})")
            continue

        logger.debug(f"Found installed version {ver!s}")
        yield ver


def pyenv_install(v: PyVer) -> str:
    """Install a python version."""
    return pyenv_execute("install", "--force", str(v))


def pyenv_uninstall(v: PyVer) -> str:
    """Install a python version."""
    return pyenv_execute("uninstall", "--force", str(v))


def pyenv_set_shims(*versions: PyVer) -> str:
    """Set shim priority."""
    return pyenv_execute("global", "system", *(str(v) for v in versions))
