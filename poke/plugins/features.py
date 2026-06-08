from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES

@Client.on_message(filters.command("features", prefixes=PREFIXES))
async def features_handler(c: Client, m: Message):
    _user = await c.get_me()


    if _user.id != m.from_user.id:
        return

    text = (
        "Features\n\n"

        "start / stop\n"
        "start begins auto hunting loop\n"
        "stop ends the current hunting loop\n\n"

        "mode\n"
        "mode poke focuses on catching pokemon\n"
        "mode pd focuses on earning pokedollars\n\n"

        "pattern\n"
        "controls button clicking pattern\n"
        "1 to 4 decide how many buttons are used randomly\n\n"

        "run\n"
        "run from specific pokemon types\n"
        "example run ice will skip ice type pokemon\n"
        "run off disables this\n\n"

        "auto hunt system\n"
        "detects wild pokemon and reacts automatically\n"
        "can attack catch or run based on settings\n\n"

        "check\n"
        "check shows pokedollars hunts caught uptime and ping"
    )

    await m.reply(text)

