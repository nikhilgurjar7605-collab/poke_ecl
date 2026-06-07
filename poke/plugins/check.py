from pyrogram import Client, filters
from pyrogram.types import Message

from . import users_data
from config import PREFIXES

_me_cache: dict = {}


@Client.on_message(filters.command("check", prefixes=PREFIXES))
async def check_handler(c: Client, m: Message):
    user_id = m.from_user.id

    if c.me is None:
        await c.get_me()
    if c.me.id != user_id:
        return

    await m.reply(
        f"PokéDollars: {users_data['poke_dollars']}\n"
        f"Hunts: {users_data['total_hunts']}"
    )