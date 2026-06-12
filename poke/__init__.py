from pyrogram import Client
from config import API_HASH, API_ID, SESSION_STRING

userbot = Client(
    "poke_ecl_new",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    plugins=dict(root = "poke.plugins")
)

# Alias for bot handler plugin compatibility
app = userbot