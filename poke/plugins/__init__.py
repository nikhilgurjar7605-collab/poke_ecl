from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import random

from pyrogram import Client
from config import BOT_USR

users_data: dict = {
    "total_hunts": 0,
    "poke_dollars": 0,
    "in_loop": False
}

active_tasks: dict = {}


class CreateTask:
    def __init__(self, user_id: int, c: Client):
        self.send_time: int = 300
        self.user_id = user_id
        self.client = c
        self.scheduler = AsyncIOScheduler()

    async def _send_msg(self):
        await asyncio.sleep(random.randint(1, 3))
        await self.client.send_message(BOT_USR, text="/hunt")

    def start(self) -> bool:
        if self.scheduler.running:
            return False
        self.scheduler.add_job(
            self._send_msg,
            "interval",
            seconds=self.send_time,
            id=f"hunt_{self.user_id}"
        )
        self.scheduler.start()
        return True

    def stop(self) -> bool:
        if not self.scheduler.running:
            return False
        self.scheduler.shutdown(wait=False)
        self.scheduler = AsyncIOScheduler()
        return True

    @property
    def is_running(self) -> bool:
        return self.scheduler.running


__all__ = ["CreateTask", "users_data", "active_tasks"]