# Handles diff parsing and review logic
import httpx
from github_auth import get_installation_access_token
from llm_client import review_with_llm
import os

GITHUB_API_URL = "https://api.github.com"

async def review_pull_request(payload):
    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]
    pr_number = pr["number"]
    token = get_installation_access_token(installation_id)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Get list of changed files
    files_url = pr["url"] + "/files"
    async with httpx.AsyncClient() as client:
        files_resp = await client.get(files_url, headers=headers)
        files_resp.raise_for_status()
        files = files_resp.json()
        for file in files:
            filename = file["filename"]
            patch = file.get("patch")
            if not patch:
                continue
            # Send diff hunk to LLM
            review = await review_with_llm(patch)
            if not review or not review.strip():
                continue
            # Post comment if LLM found issues
            await post_review_comment(repo, pr_number, filename, patch, review, headers)

async def post_review_comment(repo, pr_number, filename, patch, review, headers):
    # Find the line number for the comment (first line of the patch)
    # For simplicity, we'll comment at the first changed line
    import re
    lines = patch.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("@@"):
            m = re.match(r"@@ -\d+,?\d* \+(\d+),?\d* @@", line)
            if m:
                start_line = int(m.group(1))
                break
    else:
        start_line = 1
    comment_body = review
    comment = {
        "path": filename,
        "body": comment_body,
        "side": "RIGHT",
        "line": start_line
    }
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/comments"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=comment)
        resp.raise_for_status()
