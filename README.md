# Telegram Investment news Digest Bot

The goal is to create a simple telegram bot that will collect the latest news from the companies, that might be interested from the investment perspective and share the digest.

A simple Telegram bot built with python-telegram-bot that:
- Responds to /start and echoes any text
- Uses Finnhub API to return a small market news digest with /digest
- Has a placeholder /diverse command for future custom news

## Setup

1. Create a virtual environment (example with Homebrew Python 3.12):

   ```bash
   /opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv312
   source .venv312/bin/activate


Deploy to PythonAnywhere (manual)
---------------------------------

Local (Mac):
1. Make sure the code works locally with `python echo_bot.py`.
2. Commit and push changes:

```bash
git add .
git commit -m "Update bot"
git push
```

PythonAnywhere (Bash console):
1. Open a Bash console on PythonAnywhere.
2. Go to your project folder and pull the latest code:

```bash
cd ~/investbot
git pull
```

3. Run the bot:

```bash
python echo_bot.py
```


Verification:
- In Telegram, send `/start` and `/digest` to the bot and confirm it responds.
