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
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)

    finally:
        # If we're running on an interactive terminal (not CI), run coverage session
        # so the parallel coverage reports are combined and human-readable output is
        # printed.
        if session.interactive:
            session.notify("coverage", posargs=[])


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
        "darglint",
        "isort",
        "flake8-isort",
    )
    session.run("flake8", *args)


@session(python=python_versions[0])
def coverage(session):
    """Produce the coverage report."""
    session.install("coverage[toml]")

    if session.posargs:
        args = session.posargs

    elif any(Path().glob(".coverage.*")):
        # Combine reports produced in parallel
        session.run("coverage", "combine")
        args = ["report"]

    else:
        args = ["report"]

    session.run("coverage", *args)


# readthedocs only seems to support up to python3.8, so make sure we build our local
# copy with the same python version
@session(python="3.8")
def docs(session):
    """Build the documentation."""
    session.install("sphinx", "myst-parser", "numpydoc", "sphinx-click", "furo")
    session.install(".")
    session.run("sphinx-build", "docs", "docs/_build")


@session(python=python_versions[0])
def black(session):
    """Run the black formatter."""
    if session.posargs:
        args = session.posargs

    else:
        args = locations

    session.install("black")
    session.run("black", *args)


@session(python=python_versions[0])
def isort(session):
    """Run isort to sort imports."""
    if session.posargs:
        args = session.posargs

    else:
        args = locations

    session.install("isort")
    session.run("isort", *args)
