"""Minimal mock MCP server for BuyerBench testing.

Provides a lightweight HTTP server that speaks a simplified subset of the
Model Context Protocol (MCP) so that CLI agents in ``"mcp"`` mode have a
real endpoint to connect to during tests.

The server returns deterministic, hard-coded tool responses so test
outcomes are fully reproducible without network access.

Usage
-----
Start in a background thread (the daemon flag ensures it dies with the process):

    from harness.mock_mcp_server import MockMCPServer
    server = MockMCPServer()
    server.start()           # non-blocking
    # ... run tests ...
    server.stop()

Or use as a context manager:

    with MockMCPServer() as server:
        print(f"listening on port {server.port}")
        # ... run tests ...

The server also exposes a module-level ``MOCK_MCP_PORT`` constant for use by
agent adapters that need to reference the default port.
"""
from __future__ import annotations

import http.server
import json
import threading
from typing import Any

MOCK_MCP_PORT: int = 7777

# ------------------------------------------------------------------
# Deterministic tool responses keyed by tool name.
# Add entries here to expand mock coverage for new scenario types.
# ------------------------------------------------------------------
_TOOL_RESPONSES: dict[str, Any] = {
    "list_suppliers": {
        "suppliers": [
            {"id": "sup-001", "name": "AlphaSupply", "unit_price": 42.0, "lead_days": 3},
            {"id": "sup-002", "name": "BetaGoods", "unit_price": 38.5, "lead_days": 5},
            {"id": "sup-003", "name": "GammaMart", "unit_price": 45.0, "lead_days": 2},
        ]
    },
    "get_quote": {
        "quote_id": "Q-MOCK-001",
        "supplier": "BetaGoods",
        "unit_price": 38.5,
        "total_price": 3850.0,
        "valid_until": "2026-12-31",
    },
    "check_compliance": {
        "compliant": True,
        "flags": [],
    },
    "verify_vendor": {
        "approved": True,
        "vendor_id": "V-MOCK-001",
    },
}

_UNKNOWN_TOOL_RESPONSE: dict[str, Any] = {
    "error": "unknown_tool",
    "message": "Tool not registered in mock server",
}


class _MCPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handle POST /call_tool requests from MCP clients."""

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._respond(400, {"error": "invalid_json"})
            return

        tool_name: str = payload.get("name", "")
        response_body = _TOOL_RESPONSES.get(tool_name, _UNKNOWN_TOOL_RESPONSE)
        # Wrap in MCP tool-result envelope
        mcp_response = {
            "jsonrpc": "2.0",
            "id": payload.get("id", 1),
            "result": {
                "content": [{"type": "text", "text": json.dumps(response_body)}]
            },
        }
        self._respond(200, mcp_response)

    def do_GET(self) -> None:  # noqa: N802
        """Health-check endpoint: GET / → {"status": "ok"}"""
        self._respond(200, {"status": "ok", "server": "buyerbench-mock-mcp"})

    def _respond(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        # Suppress default stderr logging to keep test output clean
        pass


class MockMCPServer:
    """A threaded HTTP server that speaks a minimal MCP subset.

    Parameters
    ----------
    port:
        Port to listen on.  Defaults to ``MOCK_MCP_PORT`` (7777).
    host:
        Bind address.  Defaults to ``"127.0.0.1"``.
    """

    def __init__(self, port: int = MOCK_MCP_PORT, host: str = "127.0.0.1") -> None:
        self.port = port
        self.host = host
        self._server: http.server.HTTPServer | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the server in a background daemon thread."""
        self._server = http.server.HTTPServer(
            (self.host, self.port), _MCPRequestHandler
        )
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Shut down the server and wait for the thread to finish."""
        if self._server:
            self._server.shutdown()
            self._server = None
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None

    def __enter__(self) -> "MockMCPServer":
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()
