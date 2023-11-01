"""Python-related Code."""

import re
from enum import Enum
from typing import ClassVar, Iterable

# import requests
# from bs4 import BeautifulSoup

PYTHON_URL = "https://www.python.org"

MainVersion = tuple[int, int]


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
    def main(self) -> MainVersion:
        """Main Version."""
        return (self.major, self.minor)

    def as_tuple(self) -> tuple[int, int, int, str, str]:
        """PyVer represented as a Tuple."""
        return (self.major, self.minor, self.patch, self.prerelease, self.build)

    def __str__(self) -> str:
        s = f"{self.major:d}.{self.minor:d}.{self.patch:d}"
        if len(self.prerelease) > 0:
            s += f"-{self.prerelease}"
        if len(self.build) > 0:
            s += f"+{self.build}"
        return s

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self!s})"

    @property
    def fixed_width(self) -> str:
        """Zero-padded representation."""
        s = f"{self.major:1d}.{self.minor:02d}.{self.patch:02d}"
        if len(self.prerelease) > 0:
            s += f"-{self.prerelease}"
        if len(self.build) > 0:
            s += f"+{self.build}"
        return s

    def __eq__(self, other: "PyVer") -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() == other.as_tuple()

    def __ne__(self, other: "PyVer") -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() != other.as_tuple()

    def __gt__(self, other: "PyVer") -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() > other.as_tuple()

    def __ge__(self, other: "PyVer") -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() >= other.as_tuple()

    def __lt__(self, other: "PyVer") -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.as_tuple() < other.as_tuple()

    def __le__(self, other: "PyVer") -> bool:
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


def python_supported_versions() -> Iterable[PyVer]:
    """Scrape the Python website for currently supported versions."""
    # versions: dict[Version, VersionStatus] = {}

    # rsp = requests.get(f"{PYTHON_URL}/downloads")
    # rsp.raise_for_status()

    # soup = BeautifulSoup(rsp.text, "html.parser")
    # for v in soup.find("div", class_="active-release-list-widget").find_all("li"):
    #     ver = Version.parse(v.find("span", class_="release-version").text + ".0")
    #     status = VersionStatus(v.find("span", class_="release-status").text)

    #     if status in [VersionStatus.BUGFIX, VersionStatus.SECURITY]:
    #         yield ver

    yield from (
        PyVer(3, 12),
        PyVer(3, 11),
        PyVer(3, 10),
        PyVer(3, 9),
        PyVer(3, 8),
    )
