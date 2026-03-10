import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Load variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to /start command."""
    await update.message.reply_text("Hi! Send me any message and I'll echo it back.")

async def digest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a simple daily market digest from Finnhub."""
    if not FINNHUB_API_KEY:
        await update.message.reply_text("FINNHUB_API_KEY is not set in .env.")
        return

    try:
        # Finnhub general market news
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

    if not articles:
        await update.message.reply_text("No news found.")
        return

    # Take top 3 articles
    top = articles[:3]

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
    # Create the bot application with your token
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("digest", digest))
    app.add_handler(CommandHandler("diverse", diverse))  


    # Message handler for any text message that is not a command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start polling Telegram for new messages
    app.run_polling()

if __name__ == "__main__":
    main()
