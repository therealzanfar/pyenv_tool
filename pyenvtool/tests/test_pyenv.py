"""Test pyenv interaction."""

from pytest_mock.plugin import MockerFixture

from pyenvtool.pyenv import pyenv_available_versions, pyenv_installed_versions
from pyenvtool.python import PyVer

PYENV_INSTALLED_OUTPUT = """system (set by /home/mattwyant/.pyenv/version)
3.11.1 (set by /home/mattwyant/.pyenv/version)
3.10.9 (set by /home/mattwyant/.pyenv/version)
3.9.16 (set by /home/mattwyant/.pyenv/version)
3.8.16 (set by /home/mattwyant/.pyenv/version)"""

PYENV_AVAILABLE_OUTPUT = """Available versions:
  3.9.0
  3.9-dev
  3.9.1
  3.9.2
  3.9.4
  3.9.5
  3.9.6
  3.9.7
  3.9.8
  3.9.9
  3.9.10
  3.9.11
  3.9.12
  3.9.13
  3.9.14
  3.9.15
  3.9.16
  3.9.17
  3.9.18
  3.10.0
  3.10-dev
  3.10.1
  3.10.2
  3.10.3
  3.10.4
  3.10.5
  3.10.6
  3.10.7
  3.10.8
  3.10.9
  3.10.10
  3.10.11
  3.10.12
  3.10.13
  3.11.0
  3.11-dev
  3.11.1
  3.11.2
  3.11.3
  3.11.4
  3.11.5
  3.11.6
  3.12.0
  3.12-dev
  3.13.0a1
  3.13-dev
  activepython-2.7.14
  activepython-3.5.4
  activepython-3.6.0
  anaconda-1.4.0
  anaconda-1.5.0
  anaconda-1.5.1
  anaconda-1.6.0
  anaconda-1.6.1
  anaconda-1.7.0
  anaconda-1.8.0
  anaconda-1.9.0
  anaconda-1.9.1
  anaconda-1.9.2
  anaconda-2.0.0
  anaconda-2.0.1"""


def test_pyenv_installed(mocker: MockerFixture) -> None:
    mock_execute = mocker.patch("pyenvtool.pyenv.pyenv_execute")
    mock_execute.return_value = PYENV_INSTALLED_OUTPUT

    installed = sorted(pyenv_installed_versions())

    assert installed == [
        PyVer(3, 8, 16),
        PyVer(3, 9, 16),
        PyVer(3, 10, 9),
        PyVer(3, 11, 1),
    ]


def test_pyenv_available(mocker: MockerFixture) -> None:
    mock_execute = mocker.patch("pyenvtool.pyenv.pyenv_execute")
    mock_execute.return_value = PYENV_AVAILABLE_OUTPUT

    available = sorted(pyenv_available_versions())

    assert available == [
        PyVer(3, 9, 0),
        PyVer(3, 9, 0, "dev"),
        PyVer(3, 9, 1),
        PyVer(3, 9, 2),
        PyVer(3, 9, 4),
        PyVer(3, 9, 5),
        PyVer(3, 9, 6),
        PyVer(3, 9, 7),
        PyVer(3, 9, 8),
        PyVer(3, 9, 9),
        PyVer(3, 9, 10),
        PyVer(3, 9, 11),
        PyVer(3, 9, 12),
        PyVer(3, 9, 13),
        PyVer(3, 9, 14),
        PyVer(3, 9, 15),
        PyVer(3, 9, 16),
        PyVer(3, 9, 17),
        PyVer(3, 9, 18),
        PyVer(3, 10, 0),
        PyVer(3, 10, 0, "dev"),
        PyVer(3, 10, 1),
        PyVer(3, 10, 2),
        PyVer(3, 10, 3),
        PyVer(3, 10, 4),
        PyVer(3, 10, 5),
        PyVer(3, 10, 6),
        PyVer(3, 10, 7),
        PyVer(3, 10, 8),
        PyVer(3, 10, 9),
        PyVer(3, 10, 10),
        PyVer(3, 10, 11),
        PyVer(3, 10, 12),
        PyVer(3, 10, 13),
        PyVer(3, 11, 0),
        PyVer(3, 11, 0, "dev"),
        PyVer(3, 11, 1),
        PyVer(3, 11, 2),
        PyVer(3, 11, 3),
        PyVer(3, 11, 4),
        PyVer(3, 11, 5),
        PyVer(3, 11, 6),
        PyVer(3, 12, 0),
        PyVer(3, 12, 0, "dev"),
        PyVer(3, 13, 0, "dev"),
    ]
