from __future__ import annotations

import asyncio

from app.tools.base import BaseTool


class CodeTool(BaseTool):
    name = "code_tool"

    async def run(self, code: str, timeout: int = 10) -> dict:
        proc = await asyncio.create_subprocess_exec(
            "python",
            "-c",
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            return {"ok": False, "error": "Execution timeout"}

        return {
            "ok": proc.returncode == 0,
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": proc.returncode,
        }
