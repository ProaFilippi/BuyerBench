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
        assert "scenarios evaluated" in result.output

    def test_run_unknown_agent_exits_nonzero(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--agent", "nonexistent-agent"])
        assert result.exit_code != 0
        assert "nonexistent-agent" in result.output or "Unknown agent" in result.output

    def test_run_dry_run_mock_agent(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["run", "--agent", "mock-agent-v1", "--dry-run", "--pillar", "1"]
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"
