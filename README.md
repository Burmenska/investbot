# Telegram Investment news Digest Bot

The goal is to create a simple telegram bot that will collect the latest news from the companies, I'm interested in from the investment perspective and share the digest.

A simple Telegram bot built with python-telegram-bot that:
- Responds to /start and echoes any text
- Uses Finnhub API to return a small market news digest with /digest
- Has a placeholder /diverse command for future custom news

## Setup

1. Create a virtual environment (example with Homebrew Python 3.12):

   ```bash
   /opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv312
   source .venv312/bin/activate


## Deploy to PythonAnywhere (manual)

Local (Mac):

bash
git add .
git commit -m "Update bot"
git push
PythonAnywhere (Bash console)

bash
cd ~/investbot
git pull
python echo_bot.py
Verify

In Telegram, send /start and /digest to confirm the new version is running.
