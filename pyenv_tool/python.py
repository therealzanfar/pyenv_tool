"""Python-related Code."""

import re
from enum import Enum
from typing import ClassVar, Iterable, Tuple

import requests
from bs4 import BeautifulSoup, Tag

PYTHON_URL = "https://www.python.org"
PYTHON_DOWNLOADS = f"{PYTHON_URL}/downloads"

MainVersion = Tuple[int, int]


class PyVer:
    """
    Reduced Implementation of a Python SemVer.

    Regular Expression adapted from the excellent work at the SemVer project:
    https://pypi.org/project/semver/ commit #68d19f5
    """

    RE_SEMVER: ClassVar[re.Pattern] = re.compile(
        r"""
            ^
            (?P<major>0|[1-9]\d*)
            (?:
                \.
                (?P<minor>0|[1-9]\d*)
                (?:
                    \.
                    (?P<patch>0|[1-9]\d*)
                )?
            )
            (?:-(?P<prerelease>
                (?:0|[1-9]\d*|\d*[a-z-][0-9a-z-]*)
                (?:\.(?:0|[1-9]\d*|\d*[a-z-][0-9a-z-]*))*
            ))?
            (?:\+(?P<build>
                [0-9a-z-]+
                (?:\.[0-9a-z-]+)*
            ))?
            $
        """,
        re.VERBOSE + re.IGNORECASE,
    )

    def __init__(  # noqa: PLR0913
        self,
        major: int,
        minor: int,
        patch: int = 0,
        prerelease: str = "",
        build: str = "",
    ) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    @property
    def main(self) -> "PyVer":
        """Main Version."""
        return self.__class__(self.major, self.minor)

    def as_tuple(self) -> Tuple[int, int, int, str, str]:
        """PyVer represented as a Tuple."""
        return (self.major, self.minor, self.patch, self.prerelease, self.build)

    def main_format(self) -> str:
        """Format just the main version part."""
        return f"{self.major:d}.{self.minor:d}"

    def __str__(self) -> str:
        s = f"{self.major:d}.{self.minor:d}.{self.patch:d}"
        if len(self.prerelease) > 0:
            s += f"-{self.prerelease}"
        if len(self.build) > 0:
            s += f"+{self.build}"
        return s

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self!s})"

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    @property
    def fixed_width(self) -> str:
        """Zero-padded representation."""
        s = f"{self.major:1d}.{self.minor:02d}.{self.patch:02d}"
        if len(self.prerelease) > 0:
            s += f"-{self.prerelease}"
        if len(self.build) > 0:
            s += f"+{self.build}"
        return s

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() == other.as_tuple()

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() != other.as_tuple()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() > other.as_tuple()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() >= other.as_tuple()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() < other.as_tuple()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() <= other.as_tuple()

    @classmethod
    def parse(cls, representation: str) -> "PyVer":
        """Parse a string representation of a SemVer."""
        if m := cls.RE_SEMVER.match(representation):
            return cls(
                int(m.group("major")),
                int(m.group("minor")),
                int(m.group("patch") or 0),
                m.group("prerelease") or "",
                m.group("build") or "",
            )

        raise ValueError(f"Invalid SemVer representation: {representation}")


class VersionStatus(str, Enum):
    """Python version support status."""

    PRERELEASE = "prerelease"
    BUGFIX = "bugfix"
    SECURITY = "security"
    UNSUPPORTED = "unsupported"


def python_supported_versions() -> Iterable[Tuple[PyVer, VersionStatus]]:
    """Scrape the Python website for currently supported versions."""
    rsp = requests.get(PYTHON_DOWNLOADS)
    rsp.raise_for_status()

    soup = BeautifulSoup(rsp.text, "html.parser")
    div = soup.find("div", class_="active-release-list-widget")
    if not isinstance(div, Tag):
        return

    lis = div.find_all("li")

    for li in lis:
        ver = PyVer.parse(li.find("span", class_="release-version").text + ".0")
        status = VersionStatus(li.find("span", class_="release-status").text)

        if status in [VersionStatus.BUGFIX, VersionStatus.SECURITY]:
            yield (ver, status)
