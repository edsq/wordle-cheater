"""Nox sessions."""
# Using nox_poetry:
# https://github.com/cjolowicz/nox-poetry
from nox_poetry import session

locations = ("src", "tests", "noxfile.py")


@session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session):
    """Run test suite for each supported python version."""
    session.install("pytest", "coverage[toml]", "pytest-cov", ".")
    session.run("pytest", "--cov")


@session(python=["3.7", "3.8", "3.9", "3.10"])
def lint(session):
    """Lint using flake8."""
    if session.posargs:
        args = session.posargs
    else:
        args = locations

    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)
