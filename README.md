# Telegram Sticker and GIF Blocker Bot

A Telegram bot that blocks specific sticker packs and GIFs in group chats.

## Features

- Ban and unban specific sticker packs
- Ban and unban specific GIFs
- Automatic deletion of messages containing banned stickers or GIFs
- List all banned sticker packs
- List all banned GIFs
- Russian language interface

## Commands

- `/start` - Get started with the bot
- `/help` - Show help information
- `/banpack` - Ban a sticker pack (reply to a sticker)
- `/unbanpack` - Unban a sticker pack (reply to a sticker)
- `/listpacks` - List all banned sticker packs
- `/bangif` - Ban a GIF (reply to a GIF)
- `/unbangif` - Unban a GIF (reply to a GIF)
- `/listgifs` - List all banned GIFs

## Setup

1. Make sure you have Python 3.8+ installed
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set the bot token as an environment variable (optional):
   ```
   export TELEGRAM_BOT_TOKEN="your_token_here"
   ```
4. Run the bot:
   ```
   python bot.py
   ```

## Deployment

This bot is configured to run on Render.com using the included `render.yaml` configuration.

## Data Storage

The bot stores banned sticker packs and GIFs in JSON files:
- `banned_packs.json` - Stores banned sticker pack names
- `banned_gifs.json` - Stores banned GIF file IDs

## Requirements

- Python 3.8+
- python-telegram-bot v20.8

## License

This project is open source and available for any use.
