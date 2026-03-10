import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BLACKLIST_TERMS = [
    "highly successful people",
    "successful people",
    "stay motivated",
    "motivation",
    "motivated",
    "mindset",
    "self-help",
    "self help",
    "self improvement",
    "self-improvement",
    "habits",
    "success habits",
    "morning routine",
    "morning routines",
    "life lessons",
    "life-changing",
    "life changing",
    "career advice",
    "career tips",
    "leadership lessons",
    "soft skills",
    "communication skills",
    "productivity hacks",
    "productivity tips",
    "time management",
    "work-life balance",
    "work life balance",
    "burnout",
    "imposter syndrome",
    "budgeting tips",
    "personal finance tips",
    "side hustle",
    "side hustles",
    "save money",
    "saving money",
    "retirement planning",
    "financial freedom",
]


def is_investing_signal(headline: str) -> bool:
    h = headline.lower()
    return not any(term in h for term in BLACKLIST_TERMS)


# Load variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to /start command."""
    await update.message.reply_text(
        "Hi! I’ll echo your messages.\n\n"
        "Commands:\n"
        "/start - this help\n"
        "/digest - daily market news\n"
        "/diverse - test command"
    )


async def digest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not FINNHUB_API_KEY:
        await update.message.reply_text("FINNHUB_API_KEY is not set in .env.")
        return

    try:
        url = "https://finnhub.io/api/v1/news"
        params = {
            "category": "general",
            "token": FINNHUB_API_KEY,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json()
    except Exception as e:
        await update.message.reply_text(f"Error fetching news: {e}")
        return

    # Filter out motivational / soft content
    filtered = [
        a for a in articles
        if is_investing_signal(a.get("headline", "") or "")
    ]
    if not filtered:
        await update.message.reply_text("No suitable news after filtering.")
        return

    # Take top 3 filtered articles
    top = filtered[:3]

    lines = ["📈 Daily Market News (Finnhub)\n"]
    for a in top:
        headline = a.get("headline", "No title")
        source = a.get("source", "")
        url = a.get("url", "")
        line = f"• {headline}"
        if source:
            line += f" [{source}]"
        if url:
            line += f"\n  {url}"
        lines.append(line)
        lines.append("")  # blank line between items

    text = "\n".join(lines)
    await update.message.reply_text(text)


async def diverse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to /diverse command."""
    await update.message.reply_text("This is the /diverse command.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in .env")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("digest", digest))
    app.add_handler(CommandHandler("diverse", diverse))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == "__main__":
    main()
