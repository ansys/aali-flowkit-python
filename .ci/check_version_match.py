# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Simple CLI script to compare version numbers."""

from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
from importlib import metadata
import itertools
import logging
import re
import sys
from typing import Literal

from packaging.version import Version as PyPIVersion
import semver

logger = logging.getLogger(__name__)


def convert2semver(ver: PyPIVersion) -> semver.Version:
    """Convert a PyPI version into a semver version.

    https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html
    """
    if ver.epoch:
        raise ValueError("Can't convert an epoch to semver")  # noqa: TRY003, EM101
    if ver.post:
        raise ValueError("Can't convert a post part to semver")  # noqa: TRY003, EM101

    pre = None if not ver.pre else "".join([str(i) for i in ver.pre])
    if pre and ver.dev:
        raise ValueError("Can't handle both a pre and a dev portion")  # noqa: TRY003, EM101
    if pre is None and ver.dev is None:
        pre = None
    else:
        pre = pre if pre is not None else f"dev{ver.dev}"

    return semver.Version(*ver.release, prerelease=pre, build=ver.local)


# keys are how PyPI defines it, values how semver defines
PRELEASE_CONVERSIONS = {"a": "alpha", "b": "beta"}
SEMVER_PRERELEASE_PATTERN = re.compile(r"^(?P<pretype>[a-zA-Z]*)(\.(?P<prenum>\d+))?$")
PYPI_PRERELEASE_PATTERN = re.compile(r"^(?P<pretype>[a-zA-Z]*)(?P<prenum>\d+)?$")


@dataclass
class SemVer:
    """A SemVer version."""

    version: str


@dataclass
class PyPI:
    """A PyPI version."""

    version: str


@dataclass
class PyPIMetadata:
    """Get the version from a PyPI metadata."""

    package: str


@dataclass
class Version:
    """A version."""

    version: semver.Version
    source: SemVer | PyPI | PyPIMetadata

    def prerelease_info(self) -> tuple[str, int] | None:
        """Get the prelease info.

        Returns:
            (str, int) of prerelease type, prerelease number

            OR

            None if not a prerelease

        """
        if not self.version.prerelease:
            return None

        if isinstance(self.source, SemVer):
            prerelease_matches = SEMVER_PRERELEASE_PATTERN.fullmatch(
                self.version.prerelease,
            )
        else:
            prerelease_matches = PYPI_PRERELEASE_PATTERN.fullmatch(
                self.version.prerelease,
            )

        if prerelease_matches is None:
            raise PrereleasePatternError(self)
        pretype = prerelease_matches.group("pretype")
        prenum = int(prerelease_matches.group("prenum") or 0)

        if not isinstance(self.source, SemVer):
            pretype = PRELEASE_CONVERSIONS.get(pretype, pretype)

        return (pretype, prenum)

    def __str__(self) -> str:
        """Get string representation of version."""
        return f"{self.version} (from {self.source})"


class PrereleasePatternError(ValueError):
    """Error if prerelease pattern does not match."""

    def __init__(self, ver: Version) -> None:  # noqa: D107
        super().__init__(
            f"The prerelease portion of '{ver}' does not match the expected pattern.",
        )


def versions_match(
    a: Version,
    b: Version,
    compare: Literal["major", "minor", "patch", "prerelease", "all"] = "all",
) -> bool:
    """Check if 2 versions match."""
    if compare == "prerelease":
        a.version = a.version.replace(build=None)
        b.version = b.version.replace(build=None)
    elif compare == "patch":
        a.version = a.version.replace(prerelease=None, build=None)
        b.version = b.version.replace(prerelease=None, build=None)
    elif compare == "minor":
        a.version = a.version.replace(patch=0, prerelease=None, build=None)
        b.version = b.version.replace(patch=0, prerelease=None, build=None)
    elif compare == "major":
        a.version = a.version.replace(minor=0, patch=0, prerelease=None, build=None)
        b.version = b.version.replace(minor=0, patch=0, prerelease=None, build=None)

    # check that major/minor/patch versions are equal
    if a.version.finalize_version() != b.version.finalize_version():
        return False

    a_pretype, a_prenum = a.prerelease_info() or (None, None)
    b_pretype, b_prenum = b.prerelease_info() or (None, None)

    if a_pretype != b_pretype:
        logger.error("Prerelease types do not match: %s != %s", a_pretype, b_pretype)
        return False
    if a_prenum != b_prenum:
        logger.error("Prerelease numbers do not match: %d != %d", a_prenum, b_prenum)
        return False
    return True


def main() -> None:
    """Cli to compare version numbers."""
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser(
        description="Compare version numbers from an arbitrary number of provided versions.",
    )
    parser.add_argument(
        "-c",
        "--compare",
        choices=["major", "minor", "patch", "prerelease", "all"],
        default="all",
        help="The portions of the provided versions to compare",
    )
    parser.add_argument(
        "-s",
        "--semver",
        action="append",
        type=SemVer,
        default=[],
        help="A true semantic version",
    )
    parser.add_argument(
        "-p",
        "--pypi",
        action="append",
        type=PyPI,
        default=[],
        help="A version compatible with PyPI metadata",
    )
    parser.add_argument(
        "-m",
        "--pypi-metadata",
        action="append",
        type=PyPIMetadata,
        default=[],
        help="Get the version of an installed python package from the metadata by its name",
    )
    args = parser.parse_args()

    all_versions = (
        [
            Version(
                semver.Version.parse(
                    s.version,
                    optional_minor_and_patch=args.compare in {"major", "minor"},
                ),
                s,
            )
            for s in args.semver
        ]
        + [Version(convert2semver(PyPIVersion(v.version)), v) for v in args.pypi]
        + [Version(convert2semver(PyPIVersion(metadata.version(p.package))), p) for p in args.pypi_metadata]
    )

    for a, b in itertools.combinations(all_versions, r=2):
        if versions_match(a, b, compare=args.compare):
            logger.debug(
                "Versions are equivalent%s: %s == %s",
                "" if args.compare == "all" else f" up to {args.compare} portion",
                a,
                b,
            )
        else:
            logger.error(
                "Versions are not equivalent%s: %s != %s",
                "" if args.compare == "all" else f" up to {args.compare} portion",
                a,
                b,
            )
            sys.exit(1)

    if args.compare == "all":
        logger.info("Provided versions are all equivalent")
    else:
        logger.info(
            "Provided versions are all equivalent up to %s portion",
            args.compare,
        )


if __name__ == "__main__":
    main()
