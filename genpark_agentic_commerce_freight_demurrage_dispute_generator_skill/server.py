# -*- coding: utf-8 -*-
"""MCP Server for Ocean Freight Demurrage OSRA-22 Dispute Dismissal Generator Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import FreightDemurrageDisputeDismissalGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "audit_demurrage_appointment_unavailability",
        "description": "Prove container demurrage fees were unlawfully assessed during periods when marine terminal had zero truck gate appointments.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "container_num": {
                    "type": "string"
                },
                "terminal_appointment_attempts": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                },
                "billed_demurrage_usd": {
                    "type": "number"
                }
            },
            "required": [
                "container_num",
                "terminal_appointment_attempts",
                "billed_demurrage_usd"
            ]
        }
    },
    {
        "name": "generate_fmc_inaccurate_invoice_charge_complaint",
        "description": "Generate formal FMC 46 C.F.R. \u00a7 541 complaint seeking full dismissal and statutory civil penalties against ocean carrier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carrier_scac": {
                    "type": "string"
                },
                "container_num": {
                    "type": "string"
                },
                "invoice_amount_usd": {
                    "type": "number"
                },
                "dispute_reasons": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "carrier_scac",
                "container_num",
                "invoice_amount_usd"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-freight-demurrage-dispute-generator-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(FreightDemurrageDisputeDismissalGenerator, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-freight-demurrage-dispute-generator-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
