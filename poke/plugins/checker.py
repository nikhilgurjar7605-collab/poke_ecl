import asyncio
import re
import random
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_USR
from . import users_data, CreateTask

logger = logging.getLogger(__name__)

pattern: dict = {
    1: [[0, 0]],
    2: [[0, 0], [0, 1]],
    3: [[0, 0], [0, 1], [1, 0]],
    4: [[0, 0], [0, 1], [1, 0], [1, 1]],
}


class TextChecker:
    def __init__(self, text: str, m: Message, c: Client):
        self.text = text
        self.msg = m
        self.client = c
        self.user_id = m.from_user.id
        self.task = CreateTask(m.from_user.id, c)

    def _get_button(self, i: int, j: int) -> str | None:
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

    def _stop_task(self):
        users_data["in_loop"] = False

    async def handle(self):
        if self.text.startswith("A wild"):
            await self._click_button(0, 0)

        elif self.text.startswith("Wild"):
            type_match = re.search(r"\[\s*([^\]]+)\s*\]", self.text)
            wild_types = []

            if type_match:
                raw_types = type_match.group(1).split("/")
                wild_types = [re.sub(r"[^a-zA-Z]", "", t).lower() for t in raw_types]

            if users_data["run_from"] != None and users_data["run_from"].lower() in wild_types:
                await asyncio.sleep(1)
                await self.msg.click("Run")
                return

            ra_1, ra_2 = random.choice(pattern.get(users_data["pattern"]))

            if users_data["mode"] == "pd":
                await self._click_button(ra_1, ra_2)
            else:
                match = re.search(r"HP\s*:\s*(\d+)/(\d+)", self.text)
                min_hp = int(match.group(1))
                max_hp = int(match.group(2))
                if max_hp / 2 >= min_hp:
                    await self._click_button(2, 2)
                else:
                    await self._click_button(ra_1, ra_2)

        elif self.text.endswith("Exp."):
            users_data["total_hunts"] += 1
            match = re.search(r"\+\s*(\d+)\s*💵\s*PokéDollars", self.text)
            if match:
                users_data["poke_dollars"] += int(match.group(1))
            await self._send_hunt()

        elif self.text.endswith(("lost!", "Caught!", "fled!")) or \
                self.text == "You safely ran away from the wild Pokémon!":
            if self.text.endswith("Caught!"):
                users_data["poke_caught"] += 1
            await self._send_hunt()

        elif self.text.startswith("🌟 Choose a Pokéball to throw:"):
            await asyncio.sleep(1)
            try:
                await self.msg.click("Galactic")
            except Exception:
                await self._click_button(0, 0)

        elif self.text.endswith("(3 warns = permanent ban)."):
            logger.warning("Warning received! Stopping auto-hunt to avoid ban.")
            self._stop_task()
            from config import GC_ID
            await self.client.send_message(GC_ID, "Captcha encountered... stopping auto")


@Client.on_edited_message(filters.user(BOT_USR))
@Client.on_message(filters.user(BOT_USR))
async def bot_response(c: Client, m: Message):
    if not users_data["in_loop"]:
        return

    text = m.caption or m.text
    if not text:
        return

    checker = TextChecker(text, m, c)
    await checker.handle()