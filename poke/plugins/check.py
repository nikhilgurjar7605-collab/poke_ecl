import time
from pyrogram import Client, filters
from pyrogram.types import Message

from . import users_data
from config import PREFIXES

START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - START_TIME)
    mins, sec = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs}h {mins}m {sec}s"

@Client.on_message(filters.command("check", prefixes=PREFIXES))
async def check_handler(c: Client, m: Message):
    user_id = m.from_user.id


    _user = await c.get_me()
    if _user.id != user_id:
        return

    start = time.time()

    msg = await m.reply("checking...")

    ping = round((time.time() - start) * 1000)

    await msg.edit(
        f"Stats\n\n"
        f"PokéDollars: {users_data['poke_dollars']}\n"
        f"Hunts: {users_data['total_hunts']}\n"
        f"Pokémon Caught: {users_data['poke_caught']}\n\n"
        f"Uptime: {get_uptime()}\n"
        f"Ping: {ping} ms"
    )

