import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_USR
from . import users_data


class TextChecker:
    def __init__(self, text: str, m: Message, c: Client):
        self.text = text
        self.msg = m
        self.client = c

    async def _click_first_button(self):
        await asyncio.sleep(1)
        cb = self.msg.reply_markup.inline_keyboard[0][0].callback_data
        await self.client.request_callback_answer(
            chat_id=self.msg.chat.id,
            message_id=self.msg.id,
            callback_data=cb
        )

    async def _send_hunt(self):
        await asyncio.sleep(1)
        await self.client.send_message(BOT_USR, "/hunt")

    async def handle(self):
        if self.text.startswith("A wild") or self.text.startswith("Wild :"):
            await self._click_first_button()

        elif "Exp." in self.text:
            users_data["total_hunts"] += 1
            await self._send_hunt()

        elif "You lost!" in self.text:
            await self._send_hunt()

        elif self.msg.reply_markup:
            await self._click_first_button()

@Client.on_edited_message(filters.user(BOT_USR))
@Client.on_message(filters.user(BOT_USR))
async def bot_response(c: Client, m: Message):
    text = m.caption or m.text
    if not text:
        return

    checker = TextChecker(text, m, c)
    await checker.handle()