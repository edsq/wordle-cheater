"""Nox sessions."""
# Using nox_poetry:
# https://github.com/cjolowicz/nox-poetry
from pathlib import Path

import nox
from nox_poetry import session

python_versions = ["3.10", "3.9", "3.8", "3.7"]
nox.options.sessions = ("tests", "lint")
locations = ("src", "tests", "noxfile.py", "docs/conf.py")


@session(python=python_versions)
def tests(session):
    """Run test suite for each supported python version."""
    session.install("pytest", "coverage[toml]", "pytest-cov", ".")
    session.run("pytest", "--cov")


@session(python=python_versions[0])
def black(session):
    """Run the black formatter."""
    if session.posargs:
        args = session.posargs

    else:
        args = locations

    session.install("black")
    session.run("black", *args)


@session(python=python_versions)
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
        "darglint",
    )
    session.run("flake8", *args)


@session(python=python_versions[0])
def coverage(session):
    """Produce the coverage report."""
    if session.posargs:
        args = session.posargs

    elif any(Path().glob(".coverage.*")):
        # Combine reports produced in parallel
        session.run("coverage", "combine")

    else:
        args = ["report", "--fail-under=0"]

    session.install("coverage[toml]")
    session.run("coverage", *args)


@session(python=python_versions[0])
def docs(session):
    """Build the documentation."""
    session.install("sphinx", "numpydoc")
    session.install(".")
    session.run("sphinx-build", "docs", "docs/_build")
