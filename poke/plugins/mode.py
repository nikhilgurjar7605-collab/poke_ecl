from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES
from . import users_data

@Client.on_message(filters.command("mode", prefixes=PREFIXES))
async def mode(c:Client, m:Message):
    _user = await c.get_me()
    user_id = m.from_user.id

    if _user.id != user_id:
        return 

    mode_list = m.text.split()
    mode = mode_list[1].lower()
    if (len(mode_list) > 2) or (len(mode_list) < 2) or (mode not in ["pd","poke"]):
        return await m.reply("invalid usage:\n.mode poke/pd")
    
    users_data['mode'] = mode
    await m.reply(f"mode changed to {mode}")
    
    