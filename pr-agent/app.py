# Entry point for the PR Review Bot webhook handling
from fastapi import FastAPI, Request, Header, HTTPException
from github_auth import get_installation_access_token, verify_github_webhook
from reviewer import review_pull_request
import uvicorn
import os

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    body = await request.body()
    verify_github_webhook(body, x_hub_signature_256)
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()
    if event == "pull_request" and payload["action"] in ["opened", "synchronize", "reopened"]:
        await review_pull_request(payload)
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
