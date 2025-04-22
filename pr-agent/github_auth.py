# Handles GitHub App authentication
import os
import time
import jwt
import httpx
import base64
import hashlib
import hmac
from dotenv import load_dotenv

load_dotenv()

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_API_URL = "https://api.github.com"

def get_jwt():
    private_key = base64.b64decode(GITHUB_PRIVATE_KEY)
    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + (10 * 60),
        "iss": GITHUB_APP_ID
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

def get_installation_access_token(installation_id):
    jwt_token = get_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"{GITHUB_API_URL}/app/installations/{installation_id}/access_tokens"
    resp = httpx.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["token"]

def verify_github_webhook(payload_body, signature):
    if not GITHUB_WEBHOOK_SECRET:
        raise Exception("Webhook secret not set.")
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_sig = f"sha256={mac.hexdigest()}"
    if not hmac.compare_digest(expected_sig, signature):
        raise Exception("Invalid webhook signature.")
