from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import hashlib

app = FastAPI()

EMAIL = "23f2001375@ds.study.iitm.ac.in".strip().lower()


def solve(challenge: str) -> str:
    value = f"{challenge}:{EMAIL}"
    return hashlib.sha256(value.encode()).hexdigest()[:16]


@app.post("/")
async def mcp(request: Request):
    body = await request.json()

    method = body.get("method")

    # Initialize
    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "exam-mcp-server",
                    "version": "1.0.0"
                }
            }
        })

    # notifications/initialized
    if method == "notifications/initialized":
        return JSONResponse(status_code=200, content={})

    # tools/list
    if method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "solve_challenge",
                        "description": "Returns SHA256 challenge response.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        })

    # tools/call
    if method == "tools/call":
        headers = request.headers

        challenge = headers.get("X-Exam-Challenge", "")

        answer = solve(challenge)

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": answer
                    }
                ]
            }
        })

    return JSONResponse({
        "jsonrpc": "2.0",
        "id": body.get("id"),
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    })