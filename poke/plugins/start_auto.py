from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import CreateTask, users_data, active_tasks
from config import BOT_USR


@Client.on_message(filters.command(["start", "stop"], prefixes=PREFIXES))
async def hunt_handler(c: Client, m: Message):
    command = m.command[0].lower()
    user_id = m.from_user.id

    if c.me is None:
        await c.get_me()
    if c.me.id != user_id:
        return

    if command == "start":
        if user_id in active_tasks and active_tasks[user_id].is_running:
            await m.reply("Auto-hunt is already running.")
            return

        task = CreateTask(user_id=user_id, c=c)
        task.start()
        await task._send_msg()
        active_tasks[user_id] = task
        users_data["in_loop"] = True
        await m.reply("**Auto-hunt started!**")

    elif command == "stop":
        if user_id not in active_tasks or not active_tasks[user_id].is_running:
            await m.reply("No active auto-hunt task found.")
            return

        active_tasks[user_id].stop()
        del active_tasks[user_id]
        users_data["in_loop"] = False
        await m.reply("**Auto-hunt stopped!**")