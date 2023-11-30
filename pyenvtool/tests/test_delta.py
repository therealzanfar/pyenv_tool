"""Test the change-calculating code."""

from typing import List, Tuple

import pytest

from pyenvtool import calculate_changes
from pyenvtool.pyenv import Op
from pyenvtool.python import PyVer


@pytest.mark.parametrize(
    (
        "supported_versions",
        "available_versions",
        "installed_versions",
        "keep_bugfix",
        "remove_minor",
        "results",
    ),
    [
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 10, 5)],
            [PyVer(3, 10, 0)],
            False,
            False,
            [
                (PyVer(3, 10, 5), Op.INSTALL),
                (PyVer(3, 10, 0), Op.REMOVE),
            ],
            id="supported_upgrade_replace",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 10, 5)],
            [PyVer(3, 10, 0), PyVer(3, 10, 1)],
            False,
            False,
            [
                (PyVer(3, 10, 5), Op.INSTALL),
                (PyVer(3, 10, 1), Op.REMOVE),
                (PyVer(3, 10, 0), Op.REMOVE),
            ],
            id="supported_upgrade_remove_multiple",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 10, 5)],
            [PyVer(3, 10, 0)],
            True,
            False,
            [
                (PyVer(3, 10, 5), Op.INSTALL),
            ],
            id="supported_upgrade_add",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 10, 5)],
            [],
            True,
            False,
            [
                (PyVer(3, 10, 5), Op.INSTALL),
            ],
            id="supported_new_add",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 5, 0)],
            [PyVer(3, 5, 0)],
            False,
            False,
            [],
            id="unsupported_latest_keep",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 5, 0)],
            [PyVer(3, 5, 0)],
            False,
            True,
            [
                (PyVer(3, 5, 0), Op.REMOVE),
            ],
            id="unsupported_latest_remove",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 5, 0), PyVer(3, 5, 1)],
            [PyVer(3, 5, 0), PyVer(3, 5, 1)],
            False,
            False,
            [
                (PyVer(3, 5, 0), Op.REMOVE),
            ],
            id="unsupported_bugfix_remove",
        ),
        pytest.param(
            [PyVer(3, 10)],
            [PyVer(3, 5, 0), PyVer(3, 5, 1)],
            [PyVer(3, 5, 0), PyVer(3, 5, 1)],
            False,
            True,
            [
                (PyVer(3, 5, 1), Op.REMOVE),
                (PyVer(3, 5, 0), Op.REMOVE),
            ],
            id="unsupported_bugfix_remove_all",
        ),
    ],
)
def test_delta(  # noqa: PLR0913
    supported_versions: List[PyVer],
    available_versions: List[PyVer],
    installed_versions: List[PyVer],
    keep_bugfix: bool,
    remove_minor: bool,
    results: List[Tuple[PyVer, Op]],
) -> None:
    changes = calculate_changes(
        supported_versions,
        available_versions,
        installed_versions,
        keep_bugfix,
        remove_minor,
    )
    assert sorted(changes) == sorted(results)
