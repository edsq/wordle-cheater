"""Tests of command-line interface."""
from click.testing import CliRunner

from wordle_cheater.cli import wordle_cheat


def test_wordle_cheat_basic():
    """Basic test of wordle-cheater."""
    out_base = "Wordle Cheater :(\n\n    BEATS\n    OILED\n    \nPossible solutions:\n"
    out_1 = out_base + "elder     dynel\n"
    out_2 = out_base + "dynel     elder\n"

    runner = CliRunner()
    result = runner.invoke(wordle_cheat, ["beats oiled", "bybbb bbygy"])
    assert result.exit_code == 0
    assert result.output == out_1 or result.output == out_2


def test_wordle_cheat_simple_print():
    """Test the simple-print option."""
    runner = CliRunner()
    result = runner.invoke(
        wordle_cheat, ["--simple-print", "beats oiled", "bybbb bbygy"]
    )
    assert result.exit_code == 0
    assert result.output == "elder dynel\n" or result.output == "dynel elder\n"


if __name__ == "__main__":
    test_wordle_cheat_basic()
