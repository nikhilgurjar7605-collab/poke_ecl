"""
Management commands for PokeEclipse Auto-Hunter
20 commands to manage the userbot
"""
import time
import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES, GC_ID
from . import users_data, reset_session_stats, get_uptime, logger


@Client.on_message(filters.command("help", prefixes=PREFIXES))
async def cmd_help(c: Client, m: Message):
    """Show all available commands"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    help_text = """
**🤖 PokeEclipse Auto-Hunter - Complete Command List**

**🎮 Basic Controls:**
`.start` - Start auto hunting
`.stop` - Stop auto hunting
`.pause` - Pause the bot temporarily
`.resume` - Resume after pause
`.restart` - Restart the bot session
`.autohunt` - Toggle auto-hunt mode

**⚙️ Settings:**
`.mode <poke/pd>` - Set hunting mode (catch/dollars)
`.pattern <1-4>` - Set click pattern complexity
`.run <type/off>` - Run from specific Pokémon type
`.delay <min> <max>` - Set delay range between actions
`.blacklist <add/remove/list> <type>` - Manage type blacklist
`.interval <seconds>` - Set hunting interval
`.limit <count>` - Set hunt limit
`.target <type>` - Set target Pokémon type
`.priority <high/normal/low>` - Set priority mode
`.smart` - Toggle smart mode
`.safemode` - Enable safe mode (3-6s delays)
`.fastmode` - Enable fast mode (1-2s delays)

**📊 Statistics:**
`.stats` - Show detailed session statistics
`.check` - Quick stats check
`.history` - Show hunt history
`.reset` - Reset session statistics
`.status` - Quick status check
`.export` - Export session data to JSON

**🔧 System:**
`.ping` - Check bot response time
`.uptime` - Show bot uptime
`.version` - Show version info
`.settings` - View current settings
`.notify <on/off>` - Toggle catch notifications
`.autorestart` - Toggle auto-restart on captcha
`.info` - Show bot and session info
`.alive` - Check if bot is alive
`.logs` - View recent logs
`.eval <code>` - Evaluate Python code (owner only)

**👤 User Commands:**
`.me` - Get your Telegram info
`.myid` - Get your Telegram ID
`.time` - Get current time
`.date` - Get current date
`.setbio <text>` - Set your Telegram bio
`.setname <first> [last]` - Set your Telegram name

**🎯 Pokémon Game:**
`.hunt` - Manual hunt command
`.catch` - Manual catch command
`.ball <type>` - Select Pokéball
`.bag` - Check your bag
`.pokemon` - View your Pokémon
`.market` - Check market prices
`.daily` - Claim daily reward
`.profile` - View game profile
`.trade <user>` - Initiate trade
`.battle` - Start a battle

**👥 Group Management:**
`.tagall` - Tag all members
`.kick` - Kick a user
`.ban` - Ban a user
`.unban` - Unban a user
`.mute` - Mute a user
`.unmute` - Unmute a user
`.pin` - Pin a message
`.unpin` - Unpin a message
`.chatinfo` - Get chat information
`.promote` - Promote to admin

**💬 Message Actions:**
`.forward <chat_id>` - Forward a message
`.copy <chat_id>` - Copy without tag
`.send <chat> <msg>` - Send to specific chat
`.dm <user> <msg>` - Send DM
`.save` - Save to saved messages
`.edit <text>` - Edit your message
`.reply <text>` - Reply programmatically
`.delete [count]` - Delete messages
`.clear [count]` - Clear chat messages
`.purge` - Purge messages

**🎭 Fun & Entertainment:**
`.roll` - Roll a dice
`.coin` - Flip a coin
`.random <min> <max>` - Random number
`.joke` - Tell a joke
`.quote` - Inspirational quote
`.fact` - Random fact
`.compliment` - Get a compliment
`.motivate` - Motivational message
`.weather` - Weather update
`.love <names>` - Love calculator

**⏰ Automation:**
`.remind <min> <msg>` - Set reminder
`.schedule <HH:MM> <msg>` - Schedule message
`.autosell` - Toggle auto-sell
`.autobattle` - Toggle auto-battle

**🔐 Admin Commands:**
`.join <link>` - Join channel/group
`.leave` - Leave group
`.block` - Block a user
`.unblock` - Unblock a user
`.archive` - Archive chat
`.unarchive` - Unarchive chat
`.whois` - Get user info

**🚀 Advanced:**
`.spam <count> <text>` - Spam messages
`.fspam <count> <text>` - Fast spam
`.echo <text>` - Echo message
`.repeat <count> <text>` - Repeat message
`.type <text>` - Typing effect
`.speedtest` - Test response speed
`.inspect` - Inspect message
`.source` - Get message source
`.gcast <msg>` - Global cast
`.gucast <msg>` - Global user cast

**🛠️ Bot Control:**
`.update` - Check for updates
`.changelog` - Show changelog
`.shutdown` - Shutdown bot
    """
    await m.reply(help_text)


@Client.on_message(filters.command("pause", prefixes=PREFIXES))
async def cmd_pause(c: Client, m: Message):
    """Pause the bot"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not users_data["in_loop"]:
        return await m.reply("Bot is not running.")
    
    users_data["paused"] = True
    users_data["pause_reason"] = "Manual pause by user"
    await m.reply("⏸️ **Bot Paused**\n\nUse `.resume` to continue hunting.")


@Client.on_message(filters.command("resume", prefixes=PREFIXES))
async def cmd_resume(c: Client, m: Message):
    """Resume the bot after pause"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not users_data["paused"]:
        return await m.reply("Bot is not paused.")
    
    users_data["paused"] = False
    users_data["pause_reason"] = None
    users_data["captcha_detected"] = False
    await m.reply("▶️ **Bot Resumed**\n\nContinuing auto-hunt...")


@Client.on_message(filters.command("restart", prefixes=PREFIXES))
async def cmd_restart(c: Client, m: Message):
    """Restart the bot session"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    users_data["in_loop"] = False
    users_data["paused"] = False
    users_data["start_time"] = time.time()
    reset_session_stats()
    
    await m.reply("🔄 **Bot Restarted**\n\nSession reset. Use `.start` to begin hunting.")


@Client.on_message(filters.command("stats", prefixes=PREFIXES))
async def cmd_stats(c: Client, m: Message):
    """Show detailed statistics"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    stats = users_data["session_stats"]
    caught = users_data["poke_caught"]
    hunts = users_data["total_hunts"]
    
    # Calculate rates
    catch_rate = (caught / hunts * 100) if hunts > 0 else 0
    
    text = f"""
**📊 Session Statistics**

**Hunting:**
• Total Hunts: `{hunts}`
• Pokémon Caught: `{caught}`
• Catch Rate: `{catch_rate:.1f}%`
• Runs: `{stats['runs']}`
• Flees: `{stats['flees']}`

**Warnings:**
• Current Warnings: `{stats['warnings']}`

**Last Activity:**
• Last Catch: `{stats['last_catch'] or 'None'}`
• Favorite Type: `{stats['favorite_type'] or 'N/A'}`

**Session:**
• Uptime: `{get_uptime()}`
• Mode: `{users_data['mode']}`
• Pattern: `{users_data['pattern']}`
    """
    await m.reply(text)


@Client.on_message(filters.command("history", prefixes=PREFIXES))
async def cmd_history(c: Client, m: Message):
    """Show hunt history summary"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    text = f"""
**📜 Hunt History**

Total Sessions: 1
Current Session:
• Started: `{datetime.fromtimestamp(users_data['start_time']).strftime('%Y-%m-%d %H:%M:%S')}`
• Duration: `{get_uptime()}`
• Total Earnings: `{users_data['poke_dollars']} 💵`
• Pokémon Caught: `{users_data['poke_caught']}`
    """
    await m.reply(text)


@Client.on_message(filters.command("reset", prefixes=PREFIXES))
async def cmd_reset(c: Client, m: Message):
    """Reset session statistics"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    reset_session_stats()
    users_data["total_hunts"] = 0
    users_data["poke_dollars"] = 0
    users_data["poke_caught"] = 0
    users_data["start_time"] = time.time()
    
    await m.reply("🔄 **Statistics Reset**\n\nAll session data has been cleared.")


@Client.on_message(filters.command("ping", prefixes=PREFIXES))
async def cmd_ping(c: Client, m: Message):
    """Check bot ping"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    start = time.time()
    msg = await m.reply("Pinging...")
    ping_ms = round((time.time() - start) * 1000)
    
    await msg.edit(f"🏓 **Ping:** `{ping_ms}ms`")


@Client.on_message(filters.command("uptime", prefixes=PREFIXES))
async def cmd_uptime(c: Client, m: Message):
    """Show bot uptime"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply(f"⏱️ **Uptime:** `{get_uptime()}`")


@Client.on_message(filters.command("version", prefixes=PREFIXES))
async def cmd_version(c: Client, m: Message):
    """Show version info"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("""
**🤖 PokeEclipse Auto-Hunter**
Version: `2.0.0`
Build: `Enhanced Edition`

Features:
• CAPTCHA Detection
• Auto-Pause on Warning
• Advanced Statistics
• Type Blacklisting
• Configurable Delays
    """)


@Client.on_message(filters.command("settings", prefixes=PREFIXES))
async def cmd_settings(c: Client, m: Message):
    """View current settings"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    settings = users_data["settings"]
    
    text = f"""
**⚙️ Current Settings**

**Delays:**
• Min Delay: `{settings['delay_min']}s`
• Max Delay: `{settings['delay_max']}s`

**Features:**
• Auto Restart: `{settings['auto_restart']}`
• Catch Notifications: `{settings['notify_on_catch']}`

**Blacklist:** `{settings['blacklist'] or 'Empty'}`

**Active Mode:** `{users_data['mode']}`
**Pattern:** `{users_data['pattern']}`
**Run From:** `{users_data['run_from'] or 'None'}`
    """
    await m.reply(text)


@Client.on_message(filters.command("delay", prefixes=PREFIXES))
async def cmd_delay(c: Client, m: Message):
    """Set delay range"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) != 3:
        return await m.reply("Usage: `.delay <min_seconds> <max_seconds>`\nExample: `.delay 2 5`")
    
    try:
        min_delay = int(args[1])
        max_delay = int(args[2])
        
        if min_delay < 0 or max_delay < 0:
            return await m.reply("Delays must be positive.")
        if min_delay > max_delay:
            return await m.reply("Min delay must be less than max delay.")
        
        users_data["settings"]["delay_min"] = min_delay
        users_data["settings"]["delay_max"] = max_delay
        
        await m.reply(f"✅ **Delay Updated**\nRange: `{min_delay}s - {max_delay}s`")
    except ValueError:
        await m.reply("Please enter valid numbers.")


@Client.on_message(filters.command("blacklist", prefixes=PREFIXES))
async def cmd_blacklist(c: Client, m: Message):
    """Manage type blacklist"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    
    if len(args) < 2:
        return await m.reply("Usage:\n`.blacklist add <type>`\n`.blacklist remove <type>`\n`.blacklist list`")
    
    action = args[1].lower()
    blacklist = users_data["settings"]["blacklist"]
    
    if action == "list":
        types = ", ".join(blacklist) if blacklist else "None"
        return await m.reply(f"**Blacklisted Types:** `{types}`")
    
    if len(args) < 3:
        return await m.reply("Please specify a type.")
    
    poke_type = args[2].lower()
    
    if action == "add":
        if poke_type in blacklist:
            return await m.reply(f"`{poke_type}` is already blacklisted.")
        blacklist.append(poke_type)
        await m.reply(f"✅ Added `{poke_type}` to blacklist.")
    
    elif action == "remove":
        if poke_type not in blacklist:
            return await m.reply(f"`{poke_type}` is not in blacklist.")
        blacklist.remove(poke_type)
        await m.reply(f"✅ Removed `{poke_type}` from blacklist.")
    
    else:
        await m.reply("Invalid action. Use `add`, `remove`, or `list`.")


@Client.on_message(filters.command("notify", prefixes=PREFIXES))
async def cmd_notify(c: Client, m: Message):
    """Toggle catch notifications"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        status = "ON" if users_data["settings"]["notify_on_catch"] else "OFF"
        return await m.reply(f"Current notification status: `{status}`\n\nUsage: `.notify <on/off>`")
    
    status = args[1].lower()
    if status in ["on", "true", "yes"]:
        users_data["settings"]["notify_on_catch"] = True
        await m.reply("✅ Catch notifications enabled.")
    elif status in ["off", "false", "no"]:
        users_data["settings"]["notify_on_catch"] = False
        await m.reply("❌ Catch notifications disabled.")
    else:
        await m.reply("Use `on` or `off`.")


@Client.on_message(filters.command("autorestart", prefixes=PREFIXES))
async def cmd_autorestart(c: Client, m: Message):
    """Toggle auto-restart on captcha"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    current = users_data["settings"]["auto_restart"]
    users_data["settings"]["auto_restart"] = not current
    
    status = "enabled" if not current else "disabled"
    await m.reply(f"Auto-restart {status}.")


@Client.on_message(filters.command("info", prefixes=PREFIXES))
async def cmd_info(c: Client, m: Message):
    """Show bot and session info"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    me = await c.get_me()
    
    text = f"""
**ℹ️ Bot Information**

**User:** `{me.first_name}` (`@{me.username or 'N/A'}`)
**ID:** `{me.id}`
**Status:** `{'Running' if users_data['in_loop'] else 'Stopped'}`
**Paused:** `{'Yes' if users_data.get('paused', False) else 'No'}`

**Session:**
• Started: `{datetime.fromtimestamp(users_data['start_time']).strftime('%Y-%m-%d %H:%M:%S')}`
• Uptime: `{get_uptime()}`
    """
    await m.reply(text)


@Client.on_message(filters.command("export", prefixes=PREFIXES))
async def cmd_export(c: Client, m: Message):
    """Export session data to JSON"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "stats": users_data.copy()
    }
    
    # Remove non-serializable items if any
    export_data = json.dumps(data, indent=2, default=str)
    
    await m.reply(f"```\n{export_data}\n```")


@Client.on_message(filters.command("safemode", prefixes=PREFIXES))
async def cmd_safemode(c: Client, m: Message):
    """Enable safe mode with longer delays"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    users_data["settings"]["delay_min"] = 3
    users_data["settings"]["delay_max"] = 6
    
    await m.reply("🛡️ **Safe Mode Enabled**\n\nDelays set to 3-6 seconds for safer hunting.")


@Client.on_message(filters.command("fastmode", prefixes=PREFIXES))
async def cmd_fastmode(c: Client, m: Message):
    """Enable fast mode with shorter delays"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    users_data["settings"]["delay_min"] = 1
    users_data["settings"]["delay_max"] = 2
    
    await m.reply("⚡ **Fast Mode Enabled**\n\nDelays set to 1-2 seconds for faster hunting.\n⚠️ Higher risk of detection!")


@Client.on_message(filters.command("status", prefixes=PREFIXES))
async def cmd_status(c: Client, m: Message):
    """Quick status check"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    status = "🟢 Running" if users_data["in_loop"] else "🔴 Stopped"
    if users_data.get("paused", False):
        status = "🟡 Paused"
    
    text = f"""
**📍 Bot Status**

Status: `{status}`
Mode: `{users_data['mode']}`
Pattern: `{users_data['pattern']}`
Caught: `{users_data['poke_caught']}`
Dollars: `{users_data['poke_dollars']} 💵`
Uptime: `{get_uptime()}`
    """
    await m.reply(text)
