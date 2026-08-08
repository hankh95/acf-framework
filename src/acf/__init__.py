"""ACF Framework: Graph-based AGI Certification Framework."""

from importlib.metadata import PackageNotFoundError, version as _dist_version

# Derived, never hardcoded. This attribute had drifted to "0.1.0" while the
# distribution was at 1.1.0 — `acf.__version__` and `acf --version` disagreed,
# because the CLI reads distribution metadata and this did not. Reading the same
# source removes the drift class rather than re-synchronising a second copy that
# will drift again at the next release.
try:
    __version__ = _dist_version("acf-framework")
except PackageNotFoundError:  # source checkout with no install — not an error
    __version__ = "unknown"
