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


@Client.on_message(filters.command("pattern", prefixes=PREFIXES))
async def set_pattern(c: Client, m: Message):
    user_id = m.from_user.id
    _user = await c.get_me()

    if _user.id != user_id:
        return

    if len(m.command) < 2:
        return await m.reply("usage: .pattern 1/2/3/4")

    try:
        pattern = int(m.command[1])
        if pattern not in [1, 2, 3, 4]:
            raise ValueError
    except ValueError:
        return await m.reply("pattern must be 1, 2, 3, or 4")

    users_data["pattern"] = pattern

    await m.reply(f"pattern changed to {pattern}")