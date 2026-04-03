from click.testing import CliRunner

from buyerbench.__main__ import cli


class TestDemoCommand:
    def test_demo_exits_zero(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["demo"])
        assert result.exit_code == 0, f"Non-zero exit. Output:\n{result.output}"

    def test_demo_output_contains_completion_message(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["demo"])
        assert "demo complete" in result.output.lower()

    def test_demo_output_mentions_scenarios_evaluated(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["demo"])
        assert "3 scenarios evaluated" in result.output

    def test_run_stub_not_implemented(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--agent", "test-agent"])
        assert result.exit_code == 0
        assert "not yet implemented" in result.output.lower()
