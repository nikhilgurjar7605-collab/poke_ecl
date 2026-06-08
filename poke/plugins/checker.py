import asyncio
import re
import random
import logging
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_USR, GC_ID
from . import users_data, CreateTask, get_uptime, logger

logger = logging.getLogger(__name__)

pattern: dict = {
    1: [[0, 0]],
    2: [[0, 0], [0, 1]],
    3: [[0, 0], [0, 1], [1, 0]],
    4: [[0, 0], [0, 1], [1, 0], [1, 1]],
}

# CAPTCHA detection keywords
CAPTCHA_KEYWORDS = [
    "captcha",
    "verify",
    "human",
    "click the",
    "select all",
    "warning",
    "warn",
    "ban",
    "suspicious",
    "unusual activity"
]


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
            logger.error(f"Button click error: {e}")
            return False

    async def _send_hunt(self):
        if not users_data.get("paused", False):
            await self.task.send_hunt()

    def _stop_task(self):
        users_data["in_loop"] = False

    def _pause_bot(self, reason: str):
        """Pause the bot and notify user"""
        users_data["paused"] = True
        users_data["pause_reason"] = reason
        users_data["captcha_detected"] = True
        logger.warning(f"Bot paused: {reason}")

    async def _notify_user(self, message: str):
        """Send notification to user about important events"""
        try:
            await self.client.send_message(GC_ID, message)
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    async def handle(self):
        # Check for CAPTCHA or warnings first
        text_lower = self.text.lower()
        
        for keyword in CAPTCHA_KEYWORDS:
            if keyword in text_lower:
                logger.warning(f"Potential CAPTCHA detected: {keyword}")
                self._pause_bot(f"CAPTCHA detected: {keyword}")
                await self._notify_user(
                    f"⚠️ **BOT PAUSED**\n\n"
                    f"Reason: Potential CAPTCHA or warning detected\n"
                    f"Keyword: `{keyword}`\n\n"
                    f"Please solve the CAPTCHA manually and use `.resume` to continue."
                )
                return

        if self.text.startswith("A wild"):
            await self._click_button(0, 0)

        elif self.text.startswith("Wild"):
            type_match = re.search(r"\[\s*([^\]]+)\s*\]", self.text)
            wild_types = []

            if type_match:
                raw_types = type_match.group(1).split("/")
                wild_types = [re.sub(r"[^a-zA-Z]", "", t).lower() for t in raw_types]

            # Check blacklist
            if any(poke_type in users_data["settings"]["blacklist"] for poke_type in wild_types):
                logger.info(f"Running from blacklisted type: {wild_types}")
                await asyncio.sleep(1)
                await self.msg.click("Run")
                users_data["session_stats"]["runs"] += 1
                return

            if users_data["run_from"] is not None and users_data["run_from"].lower() in wild_types:
                await asyncio.sleep(1)
                await self.msg.click("Run")
                users_data["session_stats"]["runs"] += 1
                return

            ra_1, ra_2 = random.choice(pattern.get(users_data["pattern"], [[0, 0]]))

            if users_data["mode"] == "pd":
                await self._click_button(ra_1, ra_2)
            else:
                match = re.search(r"HP\s*:\s*(\d+)/(\d+)", self.text)
                if match:
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
                users_data["session_stats"]["last_catch"] = datetime.now().isoformat()
                
                # Extract Pokémon type for stats
                type_match = re.search(r"\[([^\]]+)\]", self.text)
                if type_match:
                    poke_type = type_match.group(1).split("/")[0].strip()
                    current_fav = users_data["session_stats"]["favorite_type"]
                    if current_fav is None:
                        users_data["session_stats"]["favorite_type"] = poke_type
            
            elif self.text.endswith("fled!"):
                users_data["session_stats"]["flees"] += 1
                
            await self._send_hunt()

        elif self.text.startswith("🌟 Choose a Pokéball to throw:"):
            await asyncio.sleep(1)
            try:
                await self.msg.click("Galactic")
            except Exception:
                await self._click_button(0, 0)

        elif "(3 warns = permanent ban)" in self.text:
            logger.warning("Warning received! Stopping auto-hunt to avoid ban.")
            users_data["session_stats"]["warnings"] += 1
            self._pause_bot("Warning threshold approaching")
            await self._notify_user(
                "⚠️ **WARNING DETECTED**\n\n"
                "The bot has received a warning.\n"
                "Auto-hunt stopped to prevent permanent ban.\n"
                "Please review your activity and use `.resume` when ready."
            )


@Client.on_edited_message(filters.user(BOT_USR))
@Client.on_message(filters.user(BOT_USR))
async def bot_response(c: Client, m: Message):
    if not users_data["in_loop"]:
        return
    
    if users_data.get("paused", False):
        return

    text = m.caption or m.text
    if not text:
        return

    checker = TextChecker(text, m, c)
    await checker.handle()
