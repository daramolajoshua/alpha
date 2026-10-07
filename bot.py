import os
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
from telegram.ext import ContextTypes
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables from Railway
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@FXPulseCentral")  # Your channel username or ID

DISCLAIMER = "\n\n⚠️ *Disclaimer:* For informational and educational purposes only. Not financial advice."

async def start(update, context):
    await update.message.reply_text(
        "Welcome to ApexForex_bot! 📈\n"
        "Your real-time forex market assistant. Track live currency pairs, get pip updates, market alerts, and instant session data.\n"
        "Use /rates for live currency updates or /calendar for economic events."
        f"{DISCLAIMER}", parse_mode="Markdown"
    )

async def rates(update, context):
    text = (
        "📈 *Live Currency Exchange Rates*\n\n"
        "• *EUR/USD*: 1.0942 (+0.15%)\n"
        "• *GBP/USD*: 1.3120 (-0.08%)\n"
        "• *USD/JPY*: 149.85 (+0.32%)\n"
        f"{DISCLAIMER}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def calendar(update, context):
    text = (
        "📅 *Economic Calendar (Today)*\n\n"
        "🔴 *USD* - Non-Farm Employment Change (12:30 GMT)\n"
        "🟡 *EUR* - German Retail Sales (06:00 GMT)\n"
        f"{DISCLAIMER}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def sessions(update, context):
    text = (
        "🌍 *Global Trading Sessions*\n\n"
        "🟢 *London Session*: OPEN\n"
        "🟢 *New York Session*: OPEN\n"
        "🔴 *Sydney Session*: CLOSED\n"
        f"{DISCLAIMER}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# Automated broadcast job running every 30 minutes (1800 seconds)
async def broadcast_market_update(context: ContextTypes.DEFAULT_TYPE):
    broadcast_text = (
        "⚡ *ApexFX Auto Market Update*\n\n"
        "• *EUR/USD*: 1.0942\n"
        "• *GBP/USD*: 1.3120\n"
        "• *Market Status*: London & New York Sessions Active.\n"
        f"{DISCLAIMER}"
    )
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=broadcast_text, parse_mode="Markdown")
        logger.info("Automatic 30-minute market update broadcasted successfully.")
    except Exception as e:
        logger.error(f"Failed to broadcast update: {e}")

def main():
    if not TOKEN:
        logger.error("No BOT_TOKEN environment variable found!")
        return

    application = Application.builder().token(TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rates", rates))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(CommandHandler("sessions", sessions))

    # Job Queue for 30-minute automated channel posts (1800 seconds)
    if application.job_queue:
        application.job_queue.run_repeating(broadcast_market_update, interval=1800, first=10)

    logger.info("ApexForex_bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
