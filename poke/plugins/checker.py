import asyncio
import re
import random
import logging

from pyrogram import Client, filters
from pyrogram.types import Message


from config import BOT_USR
from . import users_data, CreateTask

logger = logging.getLogger(__name__)


class TextChecker:
    def __init__(self, text: str, m: Message, c: Client):
        self.text = text
        self.msg = m
        self.client = c
        self.task = CreateTask(m.from_user.id, c)

    def _get_button(self, i: int, j: int) -> str | None:
        """Safely retrieve callback_data from inline keyboard, returns None if missing."""
        try:
            markup = self.msg.reply_markup
            if markup is None:
                return None
            keyboard = markup.inline_keyboard
            if i >= len(keyboard) or j >= len(keyboard[i]):
                return None
            return keyboard[i][j].callback_data
        except (AttributeError, IndexError, TypeError):
            return None

    async def _click_button(self, i: int, j: int) -> bool:
        cb = self._get_button(i, j)
        if cb is None:
            logger.warning(
                "Button [%d][%d] not found on message %d — skipping click.",
                i, j, self.msg.id,
            )
            return False

        await asyncio.sleep(random.randint(1, 3))

        try:
            await self.client.request_callback_answer(
                chat_id=self.msg.chat.id,
                message_id=self.msg.id,
                callback_data=cb,
            )
            return True

        except Exception as e:
            print(e)

    async def _send_hunt(self):
        await self.task._send_msg()

    async def handle(self):
        if self.text.startswith("A wild"):
            await self._click_button(0, 0)

        elif self.text.startswith("Wild"):
            ra_1 = random.randint(0, 1)
            ra_2 = random.randint(0, 1)
            await self._click_button(ra_1, ra_2)

        elif "Exp" in self.text:
            users_data["total_hunts"] += 1

            match = re.search(r"\+\s*(\d+)\s*💵\s*PokéDollars", self.text)
            if match:
                users_data["poke_dollars"] += int(match.group(1))

            await self._send_hunt()

        elif "You lost!" in self.text:
            await self._send_hunt()
        
        elif self.text.startswith("Your"):
            return

        else:
            return


@Client.on_edited_message(filters.user(BOT_USR))
@Client.on_message(filters.user(BOT_USR))
async def bot_response(c: Client, m: Message):
    if users_data['in_loop'] == False:
        return
    text = m.caption or m.text
    if not text:
        return

    checker = TextChecker(text, m, c)
    await checker.handle()