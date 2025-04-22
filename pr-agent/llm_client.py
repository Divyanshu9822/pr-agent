import os
import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

SYSTEM_PROMPT = """
You are a helpful code reviewer. Given a diff hunk, identify issues, bugs, anti-patterns, or improvements. Reply only if there is something to comment on. If suggesting a fix, include GitHub’s code suggestion block.
"""

async def review_with_llm(diff_hunk):
    if LLM_PROVIDER == "openai":
        return await review_with_openai(diff_hunk)
    elif LLM_PROVIDER == "anthropic":
        return await review_with_anthropic(diff_hunk)
    else:
        raise ValueError("Unsupported LLM provider")

async def review_with_openai(diff_hunk):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review this code diff:\n{diff_hunk}"}
        ],
        "max_tokens": 512,
        "temperature": 0.2
    }
    timeout = httpx.Timeout(60.0)  # 60 seconds
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

async def review_with_anthropic(diff_hunk):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": LLM_MODEL,
        "max_tokens": 512,
        "temperature": 0.2,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"Review this code diff:\n{diff_hunk}"}
        ]
    }
    timeout = httpx.Timeout(60.0)  # 60 seconds
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["content"]
