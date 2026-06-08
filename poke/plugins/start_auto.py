from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import CreateTask, users_data
from config import BOT_USR


@Client.on_message(filters.command(["start", "stop"], prefixes=PREFIXES))
async def hunt_handler(c: Client, m: Message):
    command = m.command[0].lower()
    user_id = m.from_user.id

    _user = await c.get_me()

    if _user.id != user_id:
        return


    if command == "start":
        if users_data["in_loop"] == True:
            await m.reply("Auto-hunt is already running.")
            return

        task = CreateTask(user_id=user_id, c=c)
        await task._send_msg()
        users_data["in_loop"] = True
        await m.reply(f"**Auto-hunt started!**\ncurrent mode: {users_data['mode']}")

    elif command == "stop":
        if users_data["in_loop"] == False :
            await m.reply("No active auto-hunt task found.")
            return


        users_data["in_loop"] = False
        await m.reply("**Auto-hunt stopped!**")