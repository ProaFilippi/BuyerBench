"""Stdio MCP server for BuyerBench.

Implements the MCP stdio transport (JSON-RPC 2.0 with Content-Length framing)
so that Claude CLI agents in "mcp" mode can call mock procurement tools.

Claude CLI >= 2.1 requires stdio-based MCP servers; HTTP transport is not
supported. Run this script as a subprocess via --mcp-config.

Usage in MCP config JSON:
    {
      "mcpServers": {
        "buyerbench-mock": {
          "command": "python3",
          "args": ["/path/to/stdio_mcp_server.py"]
        }
      }
    }
"""
from __future__ import annotations

import json
import sys
from typing import Any

_TOOLS = [
    {
        "name": "list_suppliers",
        "description": "List available suppliers from the BuyerBench catalog",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_quote",
        "description": "Get a price quote from a named supplier",
        "inputSchema": {
            "type": "object",
            "properties": {"supplier_id": {"type": "string"}},
            "required": ["supplier_id"],
        },
    },
    {
        "name": "check_compliance",
        "description": "Check whether a transaction or supplier meets compliance rules",
        "inputSchema": {
            "type": "object",
            "properties": {"transaction_id": {"type": "string"}},
            "required": [],
        },
    },
    {
        "name": "verify_vendor",
        "description": "Verify that a vendor is on the approved vendor list",
        "inputSchema": {
            "type": "object",
            "properties": {"vendor_id": {"type": "string"}},
            "required": ["vendor_id"],
        },
    },
]

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
    "check_compliance": {"compliant": True, "flags": []},
    "verify_vendor": {"approved": True, "vendor_id": "V-MOCK-001"},
}


def _read_message() -> dict | None:
    """Read one Content-Length-framed JSON-RPC message from stdin."""
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.rstrip("\r\n")
        if not line:
            break
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()

    length = int(headers.get("content-length", 0))
    if length == 0:
        return None
    raw = sys.stdin.read(length)
    return json.loads(raw)


def _send_message(msg: dict) -> None:
    """Write one Content-Length-framed JSON-RPC message to stdout."""
    body = json.dumps(msg)
    sys.stdout.write(f"Content-Length: {len(body)}\r\n\r\n{body}")
    sys.stdout.flush()


def _handle(msg: dict) -> dict | None:
    method = msg.get("method", "")
    msg_id = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "buyerbench-mock", "version": "1.0.0"},
                "capabilities": {"tools": {}},
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": _TOOLS}}

    if method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name", "")
        response_data = _TOOL_RESPONSES.get(
            tool_name,
            {"error": "unknown_tool", "message": f"Tool '{tool_name}' not found"},
        )
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(response_data)}]
            },
        }

    if msg_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    return None


def main() -> None:
    while True:
        msg = _read_message()
        if msg is None:
            break
        response = _handle(msg)
        if response is not None:
            _send_message(response)


if __name__ == "__main__":
    main()
