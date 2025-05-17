import json
import logging
import os
from pathlib import Path
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable or use the hardcoded one if not available
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7733092460:AAFDHYW16CxVWMuH7QX04z2QFwzpuAXVHP8")

# File paths for data persistence
PACKS_FILE = "banned_packs.json"
GIFS_FILE = "banned_gifs.json"

def load_json(path):
    """Load banned items from JSON file"""
    try:
        if Path(path).exists():
            with open(path, "r") as f:
                return set(json.load(f))
        return set()
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return set()

def save_json(path, data):
    """Save banned items to JSON file"""
    try:
        with open(path, "w") as f:
            json.dump(list(data), f)
    except Exception as e:
        logger.error(f"Error saving to {path}: {e}")

# Load banned items on startup
banned_packs = load_json(PACKS_FILE)
banned_gifs = load_json(GIFS_FILE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when the command /start is issued."""
    await update.message.reply_text(
        "Привет! Я бот для блокировки стикеров и гифок в групповых чатах.\n\n"
        "Доступные команды:\n"
        "/banpack - Заблокировать стикерпак (ответьте на стикер)\n"
        "/unbanpack - Разблокировать стикерпак (ответьте на стикер)\n"
        "/listpacks - Показать список заблокированных стикерпаков\n"
        "/bangif - Заблокировать гифку (ответьте на гифку)\n"
        "/unbangif - Разблокировать гифку (ответьте на гифку)\n"
        "/listgifs - Показать список заблокированных гифок\n"
        "/help - Показать эту справку"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    await start(update, context)

async def banpack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a sticker pack by replying to a sticker."""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("Ответь на стикер, который хочешь заблокировать.")
            return
            
        if not update.message.reply_to_message.sticker:
            await update.message.reply_text("Это не стикер. Ответь на стикер, который хочешь заблокировать.")
            return
            
        pack = update.message.reply_to_message.sticker.set_name
        if not pack:
            await update.message.reply_text("У стикера нет названия пака.")
            return
            
        banned_packs.add(pack)
        save_json(PACKS_FILE, banned_packs)
        await update.message.reply_text(f"Стикерпак \"{pack}\" заблокирован.")
        logger.info(f"Sticker pack banned: {pack}")
    except Exception as e:
        logger.error(f"Error in banpack: {e}")
        await update.message.reply_text("Произошла ошибка при блокировке стикерпака.")

async def unbanpack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a sticker pack by replying to a sticker."""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("Ответь на стикер, который хочешь разблокировать.")
            return
            
        if not update.message.reply_to_message.sticker:
            await update.message.reply_text("Это не стикер. Ответь на стикер, который хочешь разблокировать.")
            return
            
        pack = update.message.reply_to_message.sticker.set_name
        if not pack:
            await update.message.reply_text("У стикера нет названия пака.")
            return
            
        if pack in banned_packs:
            banned_packs.remove(pack)
            save_json(PACKS_FILE, banned_packs)
            await update.message.reply_text(f"Стикерпак \"{pack}\" разблокирован.")
            logger.info(f"Sticker pack unbanned: {pack}")
        else:
            await update.message.reply_text("Этот пак не был заблокирован.")
    except Exception as e:
        logger.error(f"Error in unbanpack: {e}")
        await update.message.reply_text("Произошла ошибка при разблокировке стикерпака.")

async def listpacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all banned sticker packs."""
    try:
        if not banned_packs:
            await update.message.reply_text("Нет заблокированных стикерпаков.")
        else:
            msg = "Заблокированные паки:\n" + "\n".join(f"• {p}" for p in banned_packs)
            await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Error in listpacks: {e}")
        await update.message.reply_text("Произошла ошибка при получении списка заблокированных паков.")

async def bangif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a GIF by replying to it."""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("Ответь на гифку, которую хочешь заблокировать.")
            return
            
        if not update.message.reply_to_message.animation:
            await update.message.reply_text("Это не гифка. Ответь на гифку, которую хочешь заблокировать.")
            return
            
        file_id = update.message.reply_to_message.animation.file_unique_id
        banned_gifs.add(file_id)
        save_json(GIFS_FILE, banned_gifs)
        await update.message.reply_text("Гифка заблокирована.")
        logger.info(f"GIF banned with ID: {file_id}")
    except Exception as e:
        logger.error(f"Error in bangif: {e}")
        await update.message.reply_text("Произошла ошибка при блокировке гифки.")

async def unbangif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a GIF by replying to it."""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("Ответь на гифку, которую хочешь разблокировать.")
            return
            
        if not update.message.reply_to_message.animation:
            await update.message.reply_text("Это не гифка. Ответь на гифку, которую хочешь разблокировать.")
            return
            
        file_id = update.message.reply_to_message.animation.file_unique_id
        if file_id in banned_gifs:
            banned_gifs.remove(file_id)
            save_json(GIFS_FILE, banned_gifs)
            await update.message.reply_text("Гифка разблокирована.")
            logger.info(f"GIF unbanned with ID: {file_id}")
        else:
            await update.message.reply_text("Эта гифка не была заблокирована.")
    except Exception as e:
        logger.error(f"Error in unbangif: {e}")
        await update.message.reply_text("Произошла ошибка при разблокировке гифки.")

async def listgifs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all banned GIFs."""
    try:
        if not banned_gifs:
            await update.message.reply_text("Нет заблокированных гифок.")
        else:
            msg = "Заблокированные гифки (ID):\n" + "\n".join(f"• {g}" for g in banned_gifs)
            await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Error in listgifs: {e}")
        await update.message.reply_text("Произошла ошибка при получении списка заблокированных гифок.")

async def delete_blocked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete messages containing banned stickers or GIFs."""
    try:
        msg = update.message
        
        # Skip processing for command messages or messages without stickers/gifs
        if not msg or (not msg.sticker and not msg.animation):
            return
        
        # Check if sticker is from a banned pack
        if msg.sticker and msg.sticker.set_name in banned_packs:
            logger.info(f"Deleting message with banned sticker from pack: {msg.sticker.set_name}")
            await msg.delete()
            
        # Check if GIF is banned
        elif msg.animation and msg.animation.file_unique_id in banned_gifs:
            logger.info(f"Deleting message with banned GIF: {msg.animation.file_unique_id}")
            await msg.delete()
    except Exception as e:
        logger.error(f"Error in delete_blocked: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error: {context.error}")

# Пинг-сервер для Replit
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

def main():
    """Start the bot."""
    try:
        # Create the Application instance
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("banpack", banpack))
        application.add_handler(CommandHandler("unbanpack", unbanpack))
        application.add_handler(CommandHandler("listpacks", listpacks))
        application.add_handler(CommandHandler("bangif", bangif))
        application.add_handler(CommandHandler("unbangif", unbangif))
        application.add_handler(CommandHandler("listgifs", listgifs))
        
        # Add message handler for content filtering (must be last in priority)
        application.add_handler(MessageHandler(filters.ALL, delete_blocked))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the web server in a separate thread to keep the bot alive
        server_thread = Thread(target=run)
        server_thread.start()
        
        # Start the Bot
        logger.info("Bot started...")
        application.run_polling()
    except Exception as e:
        logger.critical(f"Failed to start the bot: {e}")

if __name__ == "__main__":
    main()