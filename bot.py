from io import BytesIO

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

import database
from config import BOT_TOKEN, APP_ID, APP_HASH

__BOT__: Client


async def start():
    print("Starting telegram bot...")
    bot = Client('bot', APP_ID, APP_HASH, bot_token=BOT_TOKEN)

    @bot.on_message(filters.command(["start"]))
    async def start_cmd(client: Client, message: Message) -> None:
        database.subscribe(message.from_user.id)
        await message.reply('You have subscribed to updates!')

    await bot.start()
    global __BOT__
    __BOT__ = bot
    print(f"Bot started.")


async def send_message(id: int, text: str, parse_mode: ParseMode = ParseMode.DEFAULT) -> None:
    global __BOT__
    if not __BOT__: return
    await __BOT__.send_message(id, text, parse_mode=parse_mode)


async def send_text_as_file(id: int, text: str, caption: str) -> None:
    global __BOT__
    if not __BOT__: return
    buf = BytesIO()
    buf.write(text.encode('utf-8'))
    buf.seek(0)
    await __BOT__.send_document(id, buf, file_name='message.txt', caption=caption)
