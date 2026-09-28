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

# --- HELPER FUNCTION FOR POSTING ---
async def send_market_update():
    """Helper function to send the market update photo and caption to the channel."""
    try:
        post_caption = (
            "🚨 <b>ForexPilot Auto-Market Update</b> 🚨\n\n"
            "💱 <b>Pair:</b> GBP/USD\n"
            "📈 <b>Outlook:</b> Bullish Momentum\n"
            "🎯 <b>Key Level:</b> Approaching daily resistance at 1.2850.\n\n"
            "💡 <i>Stay disciplined, manage your risk properly!</i>"
        )
        
        chart_image_url = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&auto=format&fit=crop&q=60"
        
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=chart_image_url,
            caption=post_caption,
            parse_mode="HTML"
        )
        logging.info("Successfully posted update & image to channel.")
    except Exception as e:
        logging.error(f"Failed to post update to channel: {e}")

# --- AUTOMATED CHANNEL POSTER TASK (Immediate + Every 25 Minutes) ---
async def scheduled_channel_poster():
    """Posts immediately upon deployment, then repeats every 25 minutes."""
    # Give the bot 5 seconds to fully initialize its session after boot
    await asyncio.sleep(5)
    
    # 1. Post IMMEDIATELY on startup
    logging.info("Triggering initial post upon deployment...")
    await send_market_update()
    
    # 2. Enter loop to post every 25 minutes (1500 seconds)
    while True:
        await asyncio.sleep(1500)
        await send_market_update()

# --- BOT COMMANDS (Using HTML parse mode) ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "✈️ <b>Welcome to ForexPilot09_Bot!</b>\n\n"
        "Your automated co-pilot for Forex market analysis, trading setups, and real-time signals.\n\n"
        "<b>Available Commands:</b>\n"
        "📈 /signal - Get the latest BUY/SELL setup\n"
        "📊 /analysis [Pair] - View technical breakdown (e.g., EURUSD)\n"
        "💡 /risk - Read core risk-management guidance\n"
        "❓ /ask [Question] - Ask general Forex questions"
    )
    await message.answer(welcome_text, parse_mode="HTML")

@dp.message(Command("signal"))
async def cmd_signal(message: Message):
    signal_text = (
        "🚨 <b>NEW FOREX SIGNAL</b> 🚨\n\n"
        "💱 <b>Pair:</b> EUR/USD\n"
        "📊 <b>Direction:</b> BUY\n"
        "🎯 <b>Entry Price:</b> 1.0850 - 1.0855\n"
        "🛑 <b>Stop Loss (SL):</b> 1.0810 (-40 pips)\n"
        "✅ <b>Take Profit (TP):</b> 1.0930 (+80 pips)\n\n"
        "⚠️ <i>Risk Warning: Never risk more than 1-2% of your capital per trade.</i>"
    )
    await message.answer(signal_text, parse_mode="HTML")

@dp.message(Command("analysis"))
async def cmd_analysis(message: Message):
    args = message.text.split(maxsplit=1)
    pair = args[1].upper() if len(args) > 1 else "EURUSD"
    
    analysis_text = (
        f"📊 <b>Technical Analysis: {pair}</b>\n\n"
        "• <b>Trend:</b> Bullish on 4H timeframe\n"
        "• <b>Support:</b> 1.0820\n"
        "• <b>Resistance:</b> 1.0910\n"
        "• <b>RSI (14):</b> 58.4 (Neutral to Bullish)\n"
        "• <b>Summary:</b> Price is testing a key structural support zone with increasing buying volume."
    )
    await message.answer(analysis_text, parse_mode="HTML")

@dp.message(Command("risk"))
async def cmd_risk(message: Message):
    risk_text = (
        "🛡️ <b>ForexPilot Risk-Management Guidelines</b>\n\n"
        "1. <b>Position Sizing:</b> Risk a maximum of 1% to 2% of your total account balance per trade.\n"
        "2. <b>Always Use SL:</b> Never enter the market without defining your exit point first.\n"
        "3. <b>Risk-to-Reward:</b> Aim for a minimum R:R ratio of 1:2."
    )
    await message.answer(risk_text, parse_mode="HTML")

@dp.message(Command("ask"))
async def cmd_ask(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please ask a question! Example: <code>/ask What is leverage in forex?</code>", parse_mode="HTML")
        return
    
    question = args[1]
    ai_response = (
        f"🤖 <b>ForexPilot AI Assistant</b>\n\n"
        f"<b>Q:</b> {question}\n\n"
        "<b>A:</b> In Forex trading, leverage refers to using borrowed capital from a broker to increase potential return on investment. While it magnifies profits, it equally amplifies potential losses. Always manage leverage carefully!"
    )
    await message.answer(ai_response, parse_mode="HTML")

# --- MAIN ENTRY POINT ---
async def main():
    print("ForexPilot09_Bot is starting...")
    
    # Launch the background posting task (which posts immediately, then loops every 25 min)
    asyncio.create_task(scheduled_channel_poster())
    
    # Start polling for user messages
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
