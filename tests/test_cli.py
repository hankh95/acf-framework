"""Tests for the ACF CLI."""

import json

from click.testing import CliRunner

import pytest

from acf.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestCLIBasics:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "ACF" in result.output


class TestDimensionsCommand:
    def test_list_dimensions(self, runner):
        result = runner.invoke(main, ["dimensions"])
        assert result.exit_code == 0
        assert "Breadth" in result.output
        assert "Depth" in result.output

    def test_dimensions_json(self, runner):
        result = runner.invoke(main, ["dimensions", "--json-output"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 9


class TestMeasuresCommand:
    def test_list_measures(self, runner):
        result = runner.invoke(main, ["measures"])
        assert result.exit_code == 0
        assert "66 measures total" in result.output

    def test_measures_json(self, runner):
        result = runner.invoke(main, ["measures", "--json-output"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 66


class TestLevelsCommand:
    def test_list_levels(self, runner):
        result = runner.invoke(main, ["levels"])
        assert result.exit_code == 0
        assert "Elementary" in result.output
        assert "PhD" in result.output

    def test_levels_json(self, runner):
        result = runner.invoke(main, ["levels", "--json-output"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 6


class TestInfoCommand:
    def test_info(self, runner):
        result = runner.invoke(main, ["info"])
        assert result.exit_code == 0
        assert "Dimensions: 9" in result.output
        assert "Measures:" in result.output

    def test_info_json(self, runner):
        result = runner.invoke(main, ["info", "--json-output"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["dimensions"] == 9
        assert data["measures"] == 66


class TestQueryCommand:
    def test_sparql_query(self, runner):
        result = runner.invoke(main, [
            "query",
            "SELECT ?id WHERE { ?s a acf:Dimension ; acf:id ?id . }",
        ])
        assert result.exit_code == 0
        assert "9 results" in result.output

    def test_empty_query(self, runner):
        result = runner.invoke(main, [
            "query",
            "SELECT ?x WHERE { ?x a <http://nothing> . }",
        ])
        assert result.exit_code == 0
        assert "No results" in result.output


class TestValidateCommand:
    def test_validate_example_data(self, runner):
        result = runner.invoke(main, ["validate", "examples/data/"])
        assert result.exit_code == 0
        assert "3 valid" in result.output

    def test_validate_single_file(self, runner):
        result = runner.invoke(main, [
            "validate",
            "examples/data/sample-experiment-run.json",
        ])
        assert result.exit_code == 0
        assert "1 valid" in result.output


class TestTemplateCommand:
    def test_experiment_run_template(self, runner):
        result = runner.invoke(main, ["template", "experiment-run"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["record_type"] == "experiment-run"
        assert "measure_id" in data
