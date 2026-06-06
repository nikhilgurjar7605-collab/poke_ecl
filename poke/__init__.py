from pyrogram import Client
from config import API_HASH, API_ID, SESSION_STRING

userbot = Client(
    "poke_ecl",
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root = "poke.plugins")
)