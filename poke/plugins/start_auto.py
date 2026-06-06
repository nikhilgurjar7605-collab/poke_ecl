from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES

from . import CreateTask
from config import BOT_USR

active_tasks: dict[int, CreateTask] = {}
 
 
@Client.on_message(filters.command(["start", "stop"], prefixes=PREFIXES))
async def hunt_handler(c: Client, m: Message):
    user_id = m.from_user.id
    command = m.command[0].lower()
 
    if command == "start":
        if user_id in active_tasks and active_tasks[user_id].is_running:
            await m.reply("Auto-hunt is already running.")
            return
 
        task = CreateTask(user_id=user_id, c=c)
        task.start()
        active_tasks[user_id] = task
        await m.reply("**Auto-hunt started!**")

        await c.send_message(BOT_USR, "/hunt")
 
    elif command == "stop":
        if user_id not in active_tasks or not active_tasks[user_id].is_running:
            await m.reply("No active auto-hunt task found.")
            return
 
        active_tasks[user_id].stop()
        del active_tasks[user_id]
        await m.reply("**Auto-hunt stopped!**")