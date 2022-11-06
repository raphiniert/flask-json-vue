import pytest

# test init-db command
def test_init_db(runner):
    # invoke command by name
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Dropped all tables" in result.output
    assert "Created all tables" in result.output
    assert "Initialized database." in result.output

    # invoke command by name with option
    result = runner.invoke(
        args=["init-db", "--auto-import", "--import-dir", "tests/json"]
    )
    assert result.exit_code == 0
    assert "Dropped all tables" in result.output
    assert "Created all tables" in result.output
    assert "Initialized database." in result.output
    assert "Importing Demo objects from tests/json/demo.json" in result.output
    assert "Imported <Demo Demo Name (1)>" in result.output
