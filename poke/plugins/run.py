from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import users_data


@Client.on_message(filters.command("run", prefixes=PREFIXES))
async def run_handler(c: Client, m: Message):
    _user = await c.get_me()

    if _user.id != m.from_user.id:
        return

    args = m.text.split()

    if len(args) != 2:
        return await m.reply("usage:\n.run <type>\nexample: .run ice\nor .run off")

    value = args[1].lower()

    if value == "off":
        users_data["run_from"] = None
        return await m.reply("run condition disabled")

    users_data["run_from"] = value
    await m.reply(f"will run from pokemon with type: {value}")