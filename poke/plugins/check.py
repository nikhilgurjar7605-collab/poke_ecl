from pyrogram import Client, filters
from pyrogram.types import Message

from . import users_data
from config import PREFIXES


@Client.on_message(filters.command("check", prefixes=PREFIXES))
async def check_handler(c: Client, m: Message):
    user_id = m.from_user.id
    c_user= await c.get_me()
    if c_user.id != user_id:
        return


    data = users_data

    await m.reply(
        f"PokéDollars: {data['poke_dollars']}\n"
        f"Hunts: {data['total_hunts']}"
    )