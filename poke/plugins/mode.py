from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import users_data


@Client.on_message(filters.command("mode", prefixes=PREFIXES))
async def set_mode(c: Client, m: Message):
    user_id = m.from_user.id
    _user = await c.get_me()

    if _user.id != user_id:
        return

    if len(m.command) < 2:
        return await m.reply("usage: .mode poke/pd")

    mode = m.command[1].lower()

    if mode not in ["pd", "poke"]:
        return await m.reply("mode must be 'pd' or 'poke'")

    users_data["mode"] = mode

    await m.reply(f"mode changed to {mode}")
