# Using nox_poetry:
# https://github.com/cjolowicz/nox-poetry
from nox_poetry import session


@session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session):
    """Run test suite for each supported python version."""
    session.install("pytest", "coverage[toml]", "pytest-cov", ".")
    session.run("pytest", "--cov")
