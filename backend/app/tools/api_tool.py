from __future__ import annotations

import httpx

from app.tools.base import BaseTool


class APITool(BaseTool):
    name = "api_tool"

    async def run(self, method: str, url: str, payload: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.request(method=method.upper(), url=url, json=payload)
        data = None
        try:
            data = response.json()
        except Exception:
            data = response.text[:2000]
        return {"ok": response.is_success, "status_code": response.status_code, "data": data}
