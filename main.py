import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@YourForexChannel")

if not TOKEN:
    raise ValueError("No BOT_TOKEN provided in environment variables!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- AUTOMATED CHANNEL POSTER TASK (Every 25 Minutes) ---
async def scheduled_channel_poster():
    """Background loop that posts an update and picture to the channel every 25 minutes."""
    # Brief initial pause after boot before the first loop execution
    await asyncio.sleep(15)
    
    while True:
        try:
            post_caption = (
                "🚨 **ForexPilot Auto-Market Update** 🚨\n\n"
                "💱 **Pair:** GBP/USD\n"
                "📈 **Outlook:** Bullish Momentum\n"
                "🎯 **Key Level:** Approaching daily resistance at 1.2850.\n\n"
                "💡 *Stay disciplined, manage your risk properly!*"
            )
            
            # Sample financial chart graphic link (replace with a custom image link or dynamic generator if needed)
            chart_image_url = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&auto=format&fit=crop&q=60"
            
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=chart_image_url,
                caption=post_caption,
                parse_mode="Markdown"
            )
            logging.info("Successfully posted scheduled update & image to channel.")
        except Exception as e:
            logging.error(f"Failed to post automated update to channel: {e}")
            
        # Wait for 25 minutes (25 minutes * 60 seconds = 1500 seconds)
        await asyncio.sleep(1500)

# --- BOT COMMANDS ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "✈️ **Welcome to ForexPilot09_Bot!**\n\n"
        "Your automated co-pilot for Forex market analysis, trading setups, and real-time signals.\n\n"
        "**Available Commands:**\n"
        "📈 /signal - Get the latest BUY/SELL setup\n"
        "📊 [Pair] /analysis - View technical breakdown (e.g., EURUSD)\n"
        "💡 /risk - Read core risk-management guidance\n"
        "❓ /ask [Question] - Ask general Forex questions"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(Command("signal"))
async def cmd_signal(message: Message):
    signal_text = (
        "🚨 **NEW FOREX SIGNAL** 🚨\n\n"
        "💱 **Pair:** EUR/USD\n"
        "📊 **Direction:** BUY\n"
        "🎯 **Entry Price:** 1.0850 - 1.0855\n"
        "🛑 **Stop Loss (SL):** 1.0810 (-40 pips)\n"
        " ✅ **Take Profit (TP):** 1.0930 (+80 pips)\n\n"
        "⚠️ *Risk Warning: Never risk more than 1-2% of your capital per trade.*"
    )
    await message.answer(signal_text, parse_mode="Markdown")

@dp.message(Command("analysis"))
async def cmd_analysis(message: Message):
    args = message.text.split(maxsplit=1)
    pair = args[1].upper() if len(args) > 1 else "EURUSD"
    
    analysis_text = (
        f"📊 **Technical Analysis: {pair}**\n\n"
        "• **Trend:** Bullish on 4H timeframe\n"
        "• **Support:** 1.0820\n"
        "• **Resistance:** 1.0910\n"
        "• **RSI (14):** 58.4 (Neutral to Bullish)\n"
        "• **Summary:** Price is testing a key structural support zone with increasing buying volume."
    )
    await message.answer(analysis_text, parse_mode="Markdown")

@dp.message(Command("risk"))
async def cmd_risk(message: Message):
    risk_text = (
        "🛡️ **ForexPilot Risk-Management Guidelines**\n\n"
        "1. **Position Sizing:** Risk a maximum of 1% to 2% of your total account balance per trade.\n"
        "2. **Always Use SL:** Never enter the market without defining your exit point first.\n"
        "3. **Risk-to-Reward:** Aim for a minimum R:R ratio of 1:2."
    )
    await message.answer(risk_text, parse_mode="Markdown")

@dp.message(Command("ask"))
async def cmd_ask(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please ask a question! Example: `/ask What is leverage in forex?`", parse_mode="Markdown")
        return
    
    question = args[1]
    ai_response = (
        f"🤖 **ForexPilot AI Assistant**\n\n"
        f"**Q:** {question}\n\n"
        "**A:** In Forex trading, leverage refers to using borrowed capital from a broker to increase potential return on investment. While it magnifies profits, it equally amplifies potential losses. Always manage leverage carefully!"
    )
    await message.answer(ai_response, parse_mode="Markdown")

# --- MAIN ENTRY POINT ---
async def main():
    print("ForexPilot09_Bot is starting...")
    
    # Launch the 25-minute channel posting loop in the background
    asyncio.create_task(scheduled_channel_poster())
    
    # Start polling for user messages
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
