from click.testing import CliRunner

from pymetrica.run_all import run_all


def test_run_all_includes_base_stats() -> None:
    result = CliRunner().invoke(
        run_all,
        ["./tests/sample_codebases/small_codebase"],
    )

    assert result.exit_code == 0
    assert "Metric: Base Stats" in result.output
    assert "files_number: 1" in result.output
