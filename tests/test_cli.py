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


class TestScoreCommand:
    def test_score_example_data(self, runner):
        result = runner.invoke(main, ["score", "examples/data/"])
        assert result.exit_code == 0
        assert "Aggregate Score" in result.output
        assert "ACF-" in result.output

    def test_score_json_output(self, runner):
        result = runner.invoke(main, ["score", "examples/data/", "--json-output"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "system_id" in data
        assert "aggregate_score" in data
        assert "certification_level" in data
        assert "dimensions" in data

    def test_score_save_profile(self, runner, tmp_path):
        out = tmp_path / "profile.json"
        result = runner.invoke(main, [
            "score", "examples/data/", "--save", str(out),
        ])
        assert result.exit_code == 0
        assert out.exists()
        data = json.loads(out.read_text())
        assert "aggregate_score" in data

    def test_score_no_data(self, runner, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        result = runner.invoke(main, ["score", str(empty)])
        assert result.exit_code == 0
        assert "No" in result.output


class TestCompareCommand:
    def test_compare_profiles(self, runner, tmp_path):
        """Test compare with two generated profiles."""
        p1 = {
            "system_id": "system-a",
            "system_type": "test",
            "version": "1.0",
            "aggregate_score": 50.0,
            "certification_level": "ACF-3",
            "dimensions": {
                "depth": {"dimension": "depth", "score": 60.0, "sub_level": "L4"},
                "breadth": {"dimension": "breadth", "score": 40.0, "sub_level": "B2"},
            },
        }
        p2 = {
            "system_id": "system-b",
            "system_type": "test",
            "version": "2.0",
            "aggregate_score": 70.0,
            "certification_level": "ACF-4",
            "dimensions": {
                "depth": {"dimension": "depth", "score": 80.0, "sub_level": "L5"},
                "breadth": {"dimension": "breadth", "score": 60.0, "sub_level": "B3"},
            },
        }
        f1 = tmp_path / "p1.json"
        f2 = tmp_path / "p2.json"
        f1.write_text(json.dumps(p1))
        f2.write_text(json.dumps(p2))

        result = runner.invoke(main, ["compare", str(f1), str(f2)])
        assert result.exit_code == 0
        assert "system-a" in result.output
        assert "system-b" in result.output
        assert "Aggregate" in result.output


class TestTemplateCommand:
    def test_experiment_run_template(self, runner):
        result = runner.invoke(main, ["template", "experiment-run"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["record_type"] == "experiment-run"
        assert "measure_id" in data
