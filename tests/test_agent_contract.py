from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from applypilot.apply.launcher import _build_agent_command


class AgentContractTests(TestCase):
    def test_codex_adapter_uses_codex_exec_and_playwright_mcp(self) -> None:
        with patch("applypilot.apply.launcher.shutil.which", return_value="/usr/local/bin/codex"):
            command = _build_agent_command(
                "codex", None, 9222, Path("/tmp/worker"), Path("/tmp/mcp.json")
            )
        self.assertEqual(command[:3], ["/usr/local/bin/codex", "exec", "--json"])
        self.assertIn("mcp_servers.playwright.command=\"npx\"", command)

    def test_claude_adapter_uses_claude_cli(self) -> None:
        with patch("applypilot.apply.launcher.shutil.which", return_value="/usr/local/bin/claude"):
            command = _build_agent_command(
                "claude", "sonnet", 9222, Path("/tmp/worker"), Path("/tmp/mcp.json")
            )
        self.assertEqual(command[:3], ["/usr/local/bin/claude", "--model", "sonnet"])
        self.assertIn("--mcp-config", command)

    def test_unknown_agent_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _build_agent_command("unknown", None, 9222, Path("/tmp/worker"), Path("/tmp/mcp.json"))
