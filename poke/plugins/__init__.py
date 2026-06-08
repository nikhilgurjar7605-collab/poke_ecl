import asyncio
import random
import time
import logging
from datetime import datetime
from typing import Optional

from pyrogram import Client
from config import BOT_USR, GC_ID

logger = logging.getLogger(__name__)

users_data: dict = {
    "total_hunts": 0,
    "poke_dollars": 0,
    "in_loop": False,
    "poke_caught": 0,
    "mode": "poke",
    "pattern": 1,
    "run_from": None,
    "start_time": time.time(),
    "paused": False,
    "pause_reason": None,
    "captcha_detected": False,
    "session_stats": {
        "runs": 0,
        "flees": 0,
        "warnings": 0,
        "last_catch": None,
        "favorite_type": None
    },
    "settings": {
        "auto_restart": False,
        "notify_on_catch": True,
        "delay_min": 1,
        "delay_max": 3,
        "blacklist": []
    }
}


class CreateTask:
    def __init__(self, user_id: int, c: Client):
        self.user_id = user_id
        self.client = c

    async def _send_msg(self, text: str = "/hunt"):
        if users_data.get("paused", False):
            logger.info("Bot is paused, not sending message")
            return False
        
        delay = random.randint(
            users_data["settings"]["delay_min"],
            users_data["settings"]["delay_max"]
        )
        await asyncio.sleep(delay)
        await self.client.send_message(BOT_USR, text=text)
        return True

    async def send_hunt(self):
        return await self._send_msg("/hunt")


def reset_session_stats():
    """Reset session statistics"""
    users_data["session_stats"] = {
        "runs": 0,
        "flees": 0,
        "warnings": 0,
        "last_catch": None,
        "favorite_type": None
    }


def get_uptime() -> str:
    """Get formatted uptime string"""
    seconds = int(time.time() - users_data["start_time"])
    mins, sec = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    
    if days > 0:
        return f"{days}d {hrs}h {mins}m {sec}s"
    elif hrs > 0:
        return f"{hrs}h {mins}m {sec}s"
    else:
        return f"{mins}m {sec}s"


__all__ = ["CreateTask", "users_data", "reset_session_stats", "get_uptime", "logger"]