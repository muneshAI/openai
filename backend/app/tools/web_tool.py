from __future__ import annotations

import httpx

from app.tools.base import BaseTool


class WebTool(BaseTool):
    name = "web_tool"

    async def run(self, url: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
        return {"ok": r.is_success, "status_code": r.status_code, "text": r.text[:5000]}
