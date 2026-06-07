from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import CreateTask, users_data, active_tasks
from config import BOT_USR


@Client.on_message(filters.command(["start", "stop"], prefixes=PREFIXES))
async def hunt_handler(c: Client, m: Message):
    command = m.command[0].lower()
    user_id = m.from_user.id

    _user = await c.get_me()

    if _user.id != user_id:
        return


    if command == "start":
        if user_id in active_tasks and active_tasks[user_id].is_running:
            await m.reply("Auto-hunt is already running.")
            return
        
        if users_data['mode'] == None:
            return await m.reply("choose a mode first")

        task = CreateTask(user_id=user_id, c=c)
        await task._send_msg()
        users_data["in_loop"] = True
        await m.reply("**Auto-hunt started!**")

    elif command == "stop":
        if users_data["in_loop"] == False :
            await m.reply("No active auto-hunt task found.")
            return


        users_data["in_loop"] = False
        await m.reply("**Auto-hunt stopped!**")