import asyncio
import random

from pyrogram import Client
from config import BOT_USR

users_data: dict = {
    "total_hunts": 0,
    "poke_dollars": 0,
    "in_loop": False,
    "poke_caught":0,
    "mode":"poke",
    "pattern":1

}



class CreateTask:
    def __init__(self, user_id: int, c: Client):
        self.user_id = user_id
        self.client = c

    async def _send_msg(self):
        await asyncio.sleep(random.randint(1, 3))
        await self.client.send_message(BOT_USR, text="/hunt")


__all__ = ["CreateTask", "users_data"]