# Claude Code Test Project

A sandbox project for exploring and testing Claude Code features, built around a Strava activity CLI tool.

## Purpose

This project is used to experiment with Claude Code — Anthropic's AI-powered CLI for software engineering tasks — including file editing, code generation, and other capabilities.

## Tools

### `strava_summary.py` — Strava Activity CLI

Fetches and displays your recent Strava activities in the terminal, including historical weather data for each activity.

**Features:**
- OAuth 2.0 authentication with automatic token refresh
- Shows distance, moving time, and elevation gain
- Fetches weather conditions at the time and location of each activity (via Open-Meteo)
- Supports displaying multiple recent activities

**Usage:**
```bash
# Show the latest activity
python strava_summary.py

# Show the last 5 activities
python strava_summary.py --count 5
```

**Setup:**
1. Create a Strava API app at https://www.strava.com/settings/api
2. Copy `.env.example` to `.env` and fill in `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`
3. Run the script — on first run it will guide you through the OAuth flow

---

### `create_presentation.py` — Strava PowerPoint Generator

Generates a styled `.pptx` presentation from your recent Strava activities, using Strava's orange brand colors.

**Features:**
- One slide per activity with stats and weather data
- Strava-branded color scheme (orange, dark gray)
- Pulls the same OAuth tokens as the CLI tool

**Usage:**
```bash
python create_presentation.py
```

## Getting Started

Install dependencies:
```bash
pip install requests python-dotenv python-pptx
```

## What I learned

- You can give Claude Code plain-language instructions directly from the chat prompt and it will plan, edit files, and run commands on your behalf.
- Prefixing a command with `!` (e.g. `! gh auth login`) runs it interactively in your terminal session, which is necessary for commands that require browser-based authentication.
- Claude Code can handle an entire git workflow end-to-end — initializing a repo, staging and committing files, installing tools like the GitHub CLI, and pushing to a remote — all from a single conversation.
