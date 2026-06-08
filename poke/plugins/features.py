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
        "check shows pokedollars hunts caught uptime and ping\n\n"

        "NEW COMMANDS:\n"
        ".help - Show all available commands\n"
        ".pause - Pause the bot temporarily\n"
        ".resume - Resume after pause\n"
        ".restart - Restart the bot session\n"
        ".stats - Show detailed session statistics\n"
        ".history - Show hunt history\n"
        ".reset - Reset session statistics\n"
        ".ping - Check bot response time\n"
        ".uptime - Show bot uptime\n"
        ".version - Show version info\n"
        ".settings - View current settings\n"
        ".delay <min> <max> - Set delay range\n"
        ".blacklist add/remove/list - Manage type blacklist\n"
        ".notify on/off - Toggle catch notifications\n"
        ".autorestart - Toggle auto-restart on captcha\n"
        ".info - Show bot and session info\n"
        ".export - Export session data to JSON\n"
        ".safemode - Enable safe mode (3-6s delays)\n"
        ".fastmode - Enable fast mode (1-2s delays)\n"
        ".status - Quick status check\n\n"

        "CAPTCHA DETECTION:\n"
        "Bot automatically detects potential CAPTCHAs and warnings\n"
        "Auto-pauses and notifies user when detected\n"
        "Use .resume after solving CAPTCHA manually"
    )

    await m.reply(text)
