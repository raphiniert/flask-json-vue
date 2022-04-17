import pytest

# test init-db command
def test_init_db(runner):
    # invoke command by name
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Initialized database." in result.output

    # invoke command by name with option
    result = runner.invoke(args=["init-db", "--auto-import"])
    assert result.exit_code == 1  # not yet implemented
