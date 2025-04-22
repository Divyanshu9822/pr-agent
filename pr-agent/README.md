# GitHub PR Review Bot App

A GitHub App written in Python that acts as a PR (Pull Request) code review bot using LLMs (OpenAI/Anthropic). It reviews code changes in PRs and posts inline review comments with actionable suggestions.

## Features
- Listens for PR events (`opened`, `synchronize`, `reopened`)
- Extracts changed files and diff hunks
- Sends code diffs to LLM (OpenAI/Anthropic) for review
- Posts inline review comments with code suggestions

## Setup
1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file based on the provided template.
3. Set up a GitHub App and obtain credentials (App ID, private key, webhook secret).
4. Run the app:
   ```bash
   uvicorn app:app --reload
   ```

## Environment Variables
```
GITHUB_APP_ID=
GITHUB_PRIVATE_KEY=
GITHUB_WEBHOOK_SECRET=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

## Deployment
- Deploy as a web service and configure your GitHub App webhook to point to `/webhook` endpoint.

## License
MIT
