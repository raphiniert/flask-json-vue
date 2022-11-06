# test export-json command
def test_export_json(runner):
    # invoke command by name with dir option
    result = runner.invoke(args=["export-json", "--export-dir", "tests/json"])
    assert result.exit_code == 0
    assert "Exporting demo to: " in result.output
    assert "tests/json/demo.json" in result.output
    assert "Exported demo." in result.output

    # invoke command by name with dir and model option
    result = runner.invoke(
        args=["export-json", "--export-dir", "tests/json", "--model", "demo"]
    )
    assert result.exit_code == 0
    assert "Filtering by model: demo" in result.output
    assert "Exporting demo to: " in result.output
    assert "tests/json/demo.json" in result.output
    assert "Exported demo." in result.output

    # invoke command by name with dir and invalid model option
    result = runner.invoke(
        args=["export-json", "--export-dir", "tests/json", "--model", "demon"]
    )
    assert result.exit_code == 0
    assert "Filtering by model: demon" in result.output
    assert "No models found." in result.output
