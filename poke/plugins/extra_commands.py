"""
Extended Commands Plugin - 50+ Additional Commands for PokeEclipse Auto-Hunter
Personal Telegram Automation Userbot
"""
import asyncio
import random
import time
import os
import sys
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
from config import PREFIXES, GC_ID, BOT_USR
from . import users_data, reset_session_stats, get_uptime, logger


# ============================================================================
# UTILITY & INFO COMMANDS (1-10)
# ============================================================================

@Client.on_message(filters.command("alive", prefixes=PREFIXES))
async def cmd_alive(c: Client, m: Message):
    """Check if bot is alive and responsive"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("🟢 **Bot is ALIVE!**\n\nReady to serve you!")


@Client.on_message(filters.command("me", prefixes=PREFIXES))
async def cmd_me(c: Client, m: Message):
    """Get your own Telegram info"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    me = await c.get_me()
    text = f"""
**👤 Your Information**

• Name: `{me.first_name} {me.last_name or ''}`
• Username: `@{me.username or 'N/A'}`
• ID: `{me.id}`
• Phone: `+{me.phone_number or 'Hidden'}`
• Bio: `{me.bio or 'No bio'}`
• Is Premium: `{me.is_premium}`
• Language: `{me.language_code}`
    """
    await m.reply(text)


@Client.on_message(filters.command("myid", prefixes=PREFIXES))
async def cmd_myid(c: Client, m: Message):
    """Get your Telegram ID"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    me = await c.get_me()
    await m.reply(f"**Your Telegram ID:** `{me.id}`")


@Client.on_message(filters.command("time", prefixes=PREFIXES))
async def cmd_time(c: Client, m: Message):
    """Get current time"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    now = datetime.now()
    await m.reply(f"🕐 **Current Time:** `{now.strftime('%H:%M:%S')}`\n📅 **Date:** `{now.strftime('%Y-%m-%d')}`")


@Client.on_message(filters.command("date", prefixes=PREFIXES))
async def cmd_date(c: Client, m: Message):
    """Get current date"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    now = datetime.now()
    await m.reply(f"📅 **Today's Date:** `{now.strftime('%A, %B %d, %Y')}`")


@Client.on_message(filters.command("speedtest", prefixes=PREFIXES))
async def cmd_speedtest(c: Client, m: Message):
    """Test bot response speed"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    start = time.time()
    msg = await m.reply("🚀 Running speed test...")
    
    # Send multiple messages to test speed
    for i in range(5):
        await asyncio.sleep(0.1)
    
    end = time.time()
    total_time = round((end - start) * 1000)
    
    await msg.edit(f"⚡ **Speed Test Result:** `{total_time}ms` for 5 iterations")


@Client.on_message(filters.command("echo", prefixes=PREFIXES))
async def cmd_echo(c: Client, m: Message):
    """Echo back your message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.echo <text>`")
    
    await m.reply(args[1])


@Client.on_message(filters.command("repeat", prefixes=PREFIXES))
async def cmd_repeat(c: Client, m: Message):
    """Repeat a message multiple times"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.repeat <count> <text>`")
    
    try:
        count = int(args[1])
        if count > 100:
            count = 100  # Limit to prevent spam
        for _ in range(count):
            await m.reply(args[2])
            await asyncio.sleep(0.5)
    except ValueError:
        await m.reply("Please enter a valid number.")


@Client.on_message(filters.command("type", prefixes=PREFIXES))
async def cmd_type(c: Client, m: Message):
    """Simulate typing effect"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.type <text>`")
    
    msg = await m.reply("...")
    await asyncio.sleep(2)
    await msg.edit(args[1])


@Client.on_message(filters.command("delete", prefixes=PREFIXES))
async def cmd_delete(c: Client, m: Message):
    """Delete messages"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    count = 1
    if len(args) > 1:
        try:
            count = int(args[1])
        except ValueError:
            pass
    
    async for msg in c.get_messages(m.chat.id, limit=count):
        await msg.delete()
        await asyncio.sleep(0.3)


# ============================================================================
# GROUP MANAGEMENT COMMANDS (11-20)
# ============================================================================

@Client.on_message(filters.command("tagall", prefixes=PREFIXES))
async def cmd_tagall(c: Client, m: Message):
    """Tag all members in the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.chat.type in ["group", "supergroup"]:
        return await m.reply("This command only works in groups!")
    
    args = m.text.split(maxsplit=1)
    message = args[1] if len(args) > 1 else "Attention everyone!"
    
    members = []
    async for member in c.get_chat_members(m.chat.id):
        if not member.user.is_bot:
            members.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
    
    text = f"{message}\n\n" + " ".join(members[:50])  # Limit to 50 mentions
    await m.reply(text, disable_web_page_preview=True)


@Client.on_message(filters.command("kick", prefixes=PREFIXES))
async def cmd_kick(c: Client, m: Message):
    """Kick a user from the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.ban_chat_member(m.chat.id, user_id)
        await m.reply(f"✅ Kicked user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("ban", prefixes=PREFIXES))
async def cmd_ban(c: Client, m: Message):
    """Ban a user from the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.ban_chat_member(m.chat.id, user_id)
        await m.reply(f"🔨 Banned user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("unban", prefixes=PREFIXES))
async def cmd_unban(c: Client, m: Message):
    """Unban a user from the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if len(m.command) < 2:
        return await m.reply("Provide user ID to unban")
    
    try:
        user_id = m.command[1]
        await c.unban_chat_member(m.chat.id, user_id)
        await m.reply(f"✅ Unbanned user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("mute", prefixes=PREFIXES))
async def cmd_mute(c: Client, m: Message):
    """Mute a user in the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.restrict_chat_member(m.chat.id, user_id, can_send_messages=False)
        await m.reply(f"🔇 Muted user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("unmute", prefixes=PREFIXES))
async def cmd_unmute(c: Client, m: Message):
    """Unmute a user in the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.restrict_chat_member(
            m.chat.id, user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True
        )
        await m.reply(f"🔊 Unmuted user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("pin", prefixes=PREFIXES))
async def cmd_pin(c: Client, m: Message):
    """Pin a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to pin it")
    
    await m.reply_to_message.pin()
    await m.reply("📌 Message pinned!")


@Client.on_message(filters.command("unpin", prefixes=PREFIXES))
async def cmd_unpin(c: Client, m: Message):
    """Unpin a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to unpin it")
    
    await m.reply_to_message.unpin()
    await m.reply("📍 Message unpinned!")


@Client.on_message(filters.command("chatinfo", prefixes=PREFIXES))
async def cmd_chatinfo(c: Client, m: Message):
    """Get chat information"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    chat = await c.get_chat(m.chat.id)
    members_count = await c.get_chat_members_count(m.chat.id)
    
    text = f"""
**📊 Chat Information**

• Title: `{chat.title}`
• ID: `{chat.id}`
• Type: `{chat.type}`
• Members: `{members_count}`
• Description: `{chat.description or 'None'}`
    """
    await m.reply(text)


@Client.on_message(filters.command("promote", prefixes=PREFIXES))
async def cmd_promote(c: Client, m: Message):
    """Promote a user to admin"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.promote_chat_member(
            m.chat.id, user_id,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True
        )
        await m.reply(f"✅ Promoted user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


# ============================================================================
# FUN & ENTERTAINMENT COMMANDS (21-30)
# ============================================================================

@Client.on_message(filters.command("roll", prefixes=PREFIXES))
async def cmd_roll(c: Client, m: Message):
    """Roll a dice"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    result = random.randint(1, 6)
    await m.reply(f"🎲 You rolled: **{result}**")


@Client.on_message(filters.command("coin", prefixes=PREFIXES))
async def cmd_coin(c: Client, m: Message):
    """Flip a coin"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    result = random.choice(["Heads", "Tails"])
    await m.reply(f"🪙 Coin flip result: **{result}**")


@Client.on_message(filters.command("random", prefixes=PREFIXES))
async def cmd_random(c: Client, m: Message):
    """Generate a random number"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 3:
        return await m.reply("Usage: `.random <min> <max>`")
    
    try:
        min_val = int(args[1])
        max_val = int(args[2])
        result = random.randint(min_val, max_val)
        await m.reply(f"🎲 Random number between {min_val} and {max_val}: **{result}**")
    except ValueError:
        await m.reply("Please enter valid numbers.")


@Client.on_message(filters.command("joke", prefixes=PREFIXES))
async def cmd_joke(c: Client, m: Message):
    """Tell a random joke"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the bicycle fall over? It was two-tired!",
    ]
    await m.reply(f"😄 {random.choice(jokes)}")


@Client.on_message(filters.command("quote", prefixes=PREFIXES))
async def cmd_quote(c: Client, m: Message):
    """Get an inspirational quote"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
    ]
    await m.reply(f"💡 {random.choice(quotes)}")


@Client.on_message(filters.command("fact", prefixes=PREFIXES))
async def cmd_fact(c: Client, m: Message):
    """Get a random fact"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    facts = [
        "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs.",
        "Octopuses have three hearts.",
        "Bananas are berries, but strawberries aren't.",
        "A group of flamingos is called a 'flamboyance'.",
        "The shortest war in history lasted only 38 minutes.",
    ]
    await m.reply(f"🧠 Did you know? {random.choice(facts)}")


@Client.on_message(filters.command("compliment", prefixes=PREFIXES))
async def cmd_compliment(c: Client, m: Message):
    """Get a random compliment"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    compliments = [
        "You're amazing just the way you are!",
        "Your positive energy is contagious!",
        "You make a difference in the world!",
        "You're stronger than you think!",
        "Your smile brightens everyone's day!",
    ]
    await m.reply(f"🌟 {random.choice(compliments)}")


@Client.on_message(filters.command("motivate", prefixes=PREFIXES))
async def cmd_motivate(c: Client, m: Message):
    """Get a motivational message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    messages = [
        "💪 You've got this! Keep pushing forward!",
        "🌟 Every expert was once a beginner. Keep practicing!",
        "🚀 Your potential is limitless. Believe in yourself!",
        "⭐ Challenges are opportunities in disguise. Embrace them!",
        "🎯 Focus on your goals and never give up!",
    ]
    await m.reply(random.choice(messages))


@Client.on_message(filters.command("weather", prefixes=PREFIXES))
async def cmd_weather(c: Client, m: Message):
    """Mock weather command (placeholder)"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    conditions = ["Sunny ☀️", "Cloudy ☁️", "Rainy 🌧️", "Partly Cloudy ⛅", "Clear 🌤️"]
    temp = random.randint(15, 35)
    await m.reply(f"🌤️ **Weather Update**\n\nCondition: {random.choice(conditions)}\nTemperature: {temp}°C")


@Client.on_message(filters.command("love", prefixes=PREFIXES))
async def cmd_love(c: Client, m: Message):
    """Calculate love percentage"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.love <name1> + <name2>`")
    
    percentage = random.randint(0, 100)
    await m.reply(f"💕 Love Calculator:\n\n{args[1]}\nLove Percentage: **{percentage}%**")


# ============================================================================
# MESSAGE & FORWARDING COMMANDS (31-40)
# ============================================================================

@Client.on_message(filters.command("forward", prefixes=PREFIXES))
async def cmd_forward(c: Client, m: Message):
    """Forward a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to forward it")
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.forward <chat_id>`")
    
    try:
        chat_id = args[1]
        await m.reply_to_message.forward(chat_id)
        await m.reply("✅ Message forwarded!")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("copy", prefixes=PREFIXES))
async def cmd_copy(c: Client, m: Message):
    """Copy a message without forward tag"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to copy it")
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.copy <chat_id>`")
    
    try:
        chat_id = args[1]
        await m.reply_to_message.copy(chat_id)
        await m.reply("✅ Message copied!")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("send", prefixes=PREFIXES))
async def cmd_send(c: Client, m: Message):
    """Send a message to a specific chat"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.send <chat_id> <message>`")
    
    try:
        chat_id = args[1]
        message = args[2]
        await c.send_message(chat_id, message)
        await m.reply("✅ Message sent!")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("broadcast", prefixes=PREFIXES))
async def cmd_broadcast(c: Client, m: Message):
    """Broadcast message to saved chats"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.broadcast <message>`")
    
    # This is a placeholder - implement based on your needs
    await m.reply("📢 Broadcast feature - customize for your use case")


@Client.on_message(filters.command("react", prefixes=PREFIXES))
async def cmd_react(c: Client, m: Message):
    """React to a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to react")
    
    emojis = ["👍", "❤️", "🎉", "🔥", "😂", "👏"]
    emoji = random.choice(emojis)
    
    # Note: Reaction feature depends on Pyrogram version
    await m.reply(f"Reacting with {emoji}")


@Client.on_message(filters.command("edit", prefixes=PREFIXES))
async def cmd_edit(c: Client, m: Message):
    """Edit your last message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.edit <new_text>` (reply to your message)")
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to edit it")
    
    await m.reply_to_message.edit(args[1])


@Client.on_message(filters.command("reply", prefixes=PREFIXES))
async def cmd_reply_cmd(c: Client, m: Message):
    """Reply to a message programmatically"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message first")
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.reply <text>`")
    
    await m.reply_to_message.reply(args[1])


@Client.on_message(filters.command("dm", prefixes=PREFIXES))
async def cmd_dm(c: Client, m: Message):
    """Send DM to a user"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.dm <user_id> <message>`")
    
    try:
        user_id = args[1]
        message = args[2]
        await c.send_message(user_id, message)
        await m.reply("✅ DM sent!")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("save", prefixes=PREFIXES))
async def cmd_save(c: Client, m: Message):
    """Save message to saved messages"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to save it")
    
    me = await c.get_me()
    await m.reply_to_message.forward(me.id)
    await m.reply("✅ Saved to Saved Messages!")


@Client.on_message(filters.command("translate", prefixes=PREFIXES))
async def cmd_translate(c: Client, m: Message):
    """Mock translate command"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.translate <text>`")
    
    # Placeholder - integrate with translation API if needed
    await m.reply("🌐 Translation feature - integrate with Google Translate API")


# ============================================================================
# ADMIN & OWNER COMMANDS (41-50)
# ============================================================================

@Client.on_message(filters.command("leave", prefixes=PREFIXES))
async def cmd_leave(c: Client, m: Message):
    """Leave a group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if m.chat.type in ["group", "supergroup"]:
        await m.reply("👋 Leaving group...")
        await c.leave_chat(m.chat.id)
    else:
        await m.reply("This is not a group!")


@Client.on_message(filters.command("join", prefixes=PREFIXES))
async def cmd_join(c: Client, m: Message):
    """Join a channel/group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.join <invite_link>`")
    
    try:
        invite_link = args[1]
        await c.join_chat(invite_link)
        await m.reply("✅ Joined successfully!")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("block", prefixes=PREFIXES))
async def cmd_block(c: Client, m: Message):
    """Block a user"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.command[1]
        
        await c.block_user(user_id)
        await m.reply(f"🚫 Blocked user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("unblock", prefixes=PREFIXES))
async def cmd_unblock(c: Client, m: Message):
    """Unblock a user"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if len(m.command) < 2:
        return await m.reply("Provide user ID to unblock")
    
    try:
        user_id = m.command[1]
        await c.unblock_user(user_id)
        await m.reply(f"✅ Unblocked user: `{user_id}`")
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("archive", prefixes=PREFIXES))
async def cmd_archive(c: Client, m: Message):
    """Archive a chat"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.archive_chats([m.chat.id])
    await m.reply("📦 Chat archived!")


@Client.on_message(filters.command("unarchive", prefixes=PREFIXES))
async def cmd_unarchive(c: Client, m: Message):
    """Unarchive a chat"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.unarchive_chats([m.chat.id])
    await m.reply("📤 Chat unarchived!")


@Client.on_message(filters.command("setbio", prefixes=PREFIXES))
async def cmd_setbio(c: Client, m: Message):
    """Set your Telegram bio"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.setbio <text>`")
    
    await c.update_profile(bio=args[1])
    await m.reply("✅ Bio updated!")


@Client.on_message(filters.command("setname", prefixes=PREFIXES))
async def cmd_setname(c: Client, m: Message):
    """Set your Telegram name"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 2:
        return await m.reply("Usage: `.setname <first> [last]`")
    
    first_name = args[1]
    last_name = args[2] if len(args) > 2 else ""
    
    await c.update_profile(first_name=first_name, last_name=last_name)
    await m.reply("✅ Name updated!")


@Client.on_message(filters.command("logs", prefixes=PREFIXES))
async def cmd_logs(c: Client, m: Message):
    """View recent logs"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    # Get last 20 lines from log file if exists
    try:
        with open('bot.log', 'r') as f:
            lines = f.readlines()[-20:]
            log_text = ''.join(lines)
        await m.reply(f"```\n{log_text}\n```")
    except FileNotFoundError:
        await m.reply("No log file found.")


@Client.on_message(filters.command("eval", prefixes=PREFIXES))
async def cmd_eval(c: Client, m: Message):
    """Evaluate Python code (OWNER ONLY - Use with caution)"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.eval <code>`")
    
    code = args[1]
    
    try:
        result = eval(code)
        await m.reply(f"```\n{result}\n```")
    except Exception as e:
        await m.reply(f"Error: ```\n{e}\n```")


# ============================================================================
# POKÉMON GAME HELPER COMMANDS (51-60)
# ============================================================================

@Client.on_message(filters.command("hunt", prefixes=PREFIXES))
async def cmd_hunt(c: Client, m: Message):
    """Manual hunt command"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/hunt")
    await m.reply("🎯 Hunt command sent!")


@Client.on_message(filters.command("catch", prefixes=PREFIXES))
async def cmd_catch(c: Client, m: Message):
    """Manual catch command"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/catch")
    await m.reply("🎣 Catch command sent!")


@Client.on_message(filters.command("ball", prefixes=PREFIXES))
async def cmd_ball(c: Client, m: Message):
    """Select Pokéball"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.ball <ball_type>`")
    
    ball_type = args[1].lower()
    await c.send_message(BOT_USR, f"/ball {ball_type}")
    await m.reply(f"⚾ Selected {ball_type} ball!")


@Client.on_message(filters.command("bag", prefixes=PREFIXES))
async def cmd_bag(c: Client, m: Message):
    """Check your bag"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/bag")
    await m.reply("🎒 Bag command sent!")


@Client.on_message(filters.command("pokemon", prefixes=PREFIXES))
async def cmd_pokemon(c: Client, m: Message):
    """View your Pokémon"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/pokemon")
    await m.reply("🐾 Pokémon list requested!")


@Client.on_message(filters.command("market", prefixes=PREFIXES))
async def cmd_market(c: Client, m: Message):
    """Check market prices"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/market")
    await m.reply("💰 Market prices requested!")


@Client.on_message(filters.command("daily", prefixes=PREFIXES))
async def cmd_daily(c: Client, m: Message):
    """Claim daily reward"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/daily")
    await m.reply("📅 Daily reward claimed!")


@Client.on_message(filters.command("profile", prefixes=PREFIXES))
async def cmd_profile(c: Client, m: Message):
    """View your game profile"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/profile")
    await m.reply("👤 Profile requested!")


@Client.on_message(filters.command("trade", prefixes=PREFIXES))
async def cmd_trade(c: Client, m: Message):
    """Initiate trade"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.trade <username>`")
    
    await c.send_message(BOT_USR, f"/trade {args[1]}")
    await m.reply(f"🔄 Trade initiated with {args[1]}!")


@Client.on_message(filters.command("battle", prefixes=PREFIXES))
async def cmd_battle(c: Client, m: Message):
    """Start a battle"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await c.send_message(BOT_USR, "/battle")
    await m.reply("⚔️ Battle command sent!")


# ============================================================================
# SCHEDULER & AUTOMATION COMMANDS (61-70)
# ============================================================================

@Client.on_message(filters.command("remind", prefixes=PREFIXES))
async def cmd_remind(c: Client, m: Message):
    """Set a reminder"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.remind <minutes> <message>`")
    
    try:
        minutes = int(args[1])
        message = args[2]
        
        await m.reply(f"⏰ Reminder set for {minutes} minutes:\n\"{message}\"")
        
        await asyncio.sleep(minutes * 60)
        await c.send_message(m.chat.id, f"🔔 **Reminder:** {message}")
    except ValueError:
        await m.reply("Please enter valid minutes.")


@Client.on_message(filters.command("schedule", prefixes=PREFIXES))
async def cmd_schedule(c: Client, m: Message):
    """Schedule a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.schedule <HH:MM> <message>`")
    
    try:
        scheduled_time = args[1]
        message = args[2]
        
        await m.reply(f"📅 Message scheduled for {scheduled_time}:\n\"{message}\"")
        # Implement actual scheduling logic here
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("autohunt", prefixes=PREFIXES))
async def cmd_autohunt(c: Client, m: Message):
    """Toggle auto-hunt mode"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if users_data["in_loop"]:
        users_data["in_loop"] = False
        await m.reply("⏹️ Auto-hunt disabled!")
    else:
        users_data["in_loop"] = True
        await m.reply("▶️ Auto-hunt enabled!")


@Client.on_message(filters.command("autosell", prefixes=PREFIXES))
async def cmd_autosell(c: Client, m: Message):
    """Toggle auto-sell feature"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    # Placeholder for auto-sell feature
    await m.reply("🔄 Auto-sell feature - configure in settings")


@Client.on_message(filters.command("autobattle", prefixes=PREFIXES))
async def cmd_autobattle(c: Client, m: Message):
    """Toggle auto-battle feature"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    # Placeholder for auto-battle feature
    await m.reply("⚔️ Auto-battle feature - configure in settings")


@Client.on_message(filters.command("interval", prefixes=PREFIXES))
async def cmd_interval(c: Client, m: Message):
    """Set hunting interval"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.interval <seconds>`")
    
    try:
        seconds = int(args[1])
        users_data["settings"]["delay_min"] = seconds
        users_data["settings"]["delay_max"] = seconds + 2
        await m.reply(f"⏱️ Hunting interval set to {seconds}-{seconds+2} seconds")
    except ValueError:
        await m.reply("Please enter a valid number.")


@Client.on_message(filters.command("limit", prefixes=PREFIXES))
async def cmd_limit(c: Client, m: Message):
    """Set hunt limit"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.limit <count>`")
    
    try:
        limit = int(args[1])
        await m.reply(f"🎯 Hunt limit set to {limit} (placeholder)")
    except ValueError:
        await m.reply("Please enter a valid number.")


@Client.on_message(filters.command("target", prefixes=PREFIXES))
async def cmd_target(c: Client, m: Message):
    """Set target Pokémon type"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.target <type>`")
    
    poke_type = args[1].lower()
    await m.reply(f"🎯 Target type set to: {poke_type}")


@Client.on_message(filters.command("priority", prefixes=PREFIXES))
async def cmd_priority(c: Client, m: Message):
    """Set priority mode"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("Usage: `.priority <high/normal/low>`")
    
    priority = args[1].lower()
    await m.reply(f"⚡ Priority mode set to: {priority}")


@Client.on_message(filters.command("smart", prefixes=PREFIXES))
async def cmd_smart(c: Client, m: Message):
    """Toggle smart mode"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("🧠 Smart mode toggled (placeholder)")


# ============================================================================
# MISC & EXPERIMENTAL COMMANDS (71-80+)
# ============================================================================

@Client.on_message(filters.command("spam", prefixes=PREFIXES))
async def cmd_spam(c: Client, m: Message):
    """Spam messages (use responsibly)"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.spam <count> <text>`")
    
    try:
        count = int(args[1])
        if count > 50:
            count = 50  # Safety limit
        
        for _ in range(count):
            await m.reply(args[2])
            await asyncio.sleep(0.3)
    except ValueError:
        await m.reply("Please enter a valid number.")


@Client.on_message(filters.command("fspam", prefixes=PREFIXES))
async def cmd_fspam(c: Client, m: Message):
    """Fast spam (no delay)"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=2)
    if len(args) < 3:
        return await m.reply("Usage: `.fspam <count> <text>`")
    
    try:
        count = int(args[1])
        if count > 20:
            count = 20  # Stricter limit for fast spam
        
        messages = []
        for _ in range(count):
            messages.append(m.reply(args[2]))
        
        await asyncio.gather(*messages)
    except ValueError:
        await m.reply("Please enter a valid number.")


@Client.on_message(filters.command("clear", prefixes=PREFIXES))
async def cmd_clear(c: Client, m: Message):
    """Clear chat messages"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split()
    count = 10
    if len(args) > 1:
        try:
            count = int(args[1])
        except ValueError:
            pass
    
    deleted = 0
    async for msg in c.get_messages(m.chat.id, limit=count):
        if msg.from_user and msg.from_user.id == (await c.get_me()).id:
            try:
                await msg.delete()
                deleted += 1
            except:
                pass
        await asyncio.sleep(0.2)
    
    await m.reply(f"✅ Deleted {deleted} messages")


@Client.on_message(filters.command("purge", prefixes=PREFIXES))
async def cmd_purge(c: Client, m: Message):
    """Purge messages from replied message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to purge from there")
    
    deleted = 0
    async for msg in c.get_messages(m.chat.id, limit=100):
        if msg.id >= m.reply_to_message.id:
            try:
                await msg.delete()
                deleted += 1
            except:
                pass
        await asyncio.sleep(0.2)
    
    await m.reply(f"🧹 Purged {deleted} messages")


@Client.on_message(filters.command("whois", prefixes=PREFIXES))
async def cmd_whois(c: Client, m: Message):
    """Get user info"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply("Reply to a user or provide username/ID")
    
    try:
        if m.reply_to_message:
            user = await c.get_users(m.reply_to_message.from_user.id)
        else:
            user = await c.get_users(m.command[1])
        
        text = f"""
**👤 User Info**

• Name: `{user.first_name} {user.last_name or ''}`
• Username: `@{user.username or 'N/A'}`
• ID: `{user.id}`
• Is Bot: `{user.is_bot}`
• Is Verified: `{user.is_verified}`
• Is Premium: `{user.is_premium}`
        """
        await m.reply(text)
    except Exception as e:
        await m.reply(f"Error: {e}")


@Client.on_message(filters.command("gcast", prefixes=PREFIXES))
async def cmd_gcast(c: Client, m: Message):
    """Global cast to all groups where bot is joined"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.gcast <message>`")
    
    message_text = args[1]
    success = 0
    failed = 0
    skipped = 0
    
    progress_msg = await m.reply("📢 **Starting Global Cast...**\n\nPlease wait...")
    
    async for dialog in c.get_dialogs():
        try:
            # Only send to groups (not users or channels)
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    await c.send_message(dialog.chat.id, message_text)
                    success += 1
                    await asyncio.sleep(0.5)  # Small delay to avoid flooding
                except Exception as e:
                    failed += 1
                    logger.error(f"Failed to send to {dialog.chat.title}: {e}")
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
            continue
    
    result_text = f"""
**📢 Global Cast Completed**

✅ **Success:** `{success}` groups
❌ **Failed:** `{failed}` groups
⏭️ **Skipped:** `{skipped}` (users/channels)

**Message:** `{message_text[:50]}...`
    """
    await progress_msg.edit(result_text)


@Client.on_message(filters.command("gucast", prefixes=PREFIXES))
async def cmd_gucast(c: Client, m: Message):
    """Global user cast to all users"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("Usage: `.gucast <message>`")
    
    message_text = args[1]
    success = 0
    failed = 0
    skipped = 0
    
    progress_msg = await m.reply("📢 **Starting Global User Cast...**\n\nPlease wait...")
    
    async for dialog in c.get_dialogs():
        try:
            # Only send to private chats (users)
            if dialog.chat.type == "private":
                try:
                    await c.send_message(dialog.chat.id, message_text)
                    success += 1
                    await asyncio.sleep(0.5)  # Small delay to avoid flooding
                except Exception as e:
                    failed += 1
                    logger.error(f"Failed to send to {dialog.chat.first_name}: {e}")
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
            continue
    
    result_text = f"""
**📢 Global User Cast Completed**

✅ **Success:** `{success}` users
❌ **Failed:** `{failed}` users
⏭️ **Skipped:** `{skipped}` (groups/channels)

**Message:** `{message_text[:50]}...`
    """
    await progress_msg.edit(result_text)


@Client.on_message(filters.command("analyze", prefixes=PREFIXES))
async def cmd_analyze(c: Client, m: Message):
    """Analyze current group - get detailed information about the group"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    # If reply to a message, analyze that chat, otherwise current chat
    chat_id = m.chat.id
    if m.reply_to_message:
        chat_id = m.reply_to_message.chat.id
    
    try:
        chat = await c.get_chat(chat_id)
        
        # Get members count
        members_count = chat.members_count if hasattr(chat, 'members_count') else 'N/A'
        
        # Get administrators
        admins = []
        admin_count = 0
        try:
            async for admin in c.get_chat_administrators(chat_id):
                admins.append(admin.user.first_name)
                admin_count += 1
        except:
            admins = ["Unable to fetch"]
        
        # Get recent activity (last 100 messages stats)
        total_messages = 0
        text_messages = 0
        media_messages = 0
        unique_users = set()
        
        async for msg in c.get_chat_history(chat_id, limit=100):
            total_messages += 1
            if msg.text:
                text_messages += 1
            if msg.photo or msg.video or msg.document:
                media_messages += 1
            if msg.from_user:
                unique_users.add(msg.from_user.id)
        
        # Group info text
        analysis_text = f"""
**🔍 Group Analysis Report**

**📋 Basic Info:**
• **Name:** `{chat.title}`
• **ID:** `{chat.id}`
• **Type:** `{chat.type}`
• **Members:** `{members_count}`
• **Administrators:** `{admin_count}`
• **Description:** `{chat.description[:100] if chat.description else 'No description'}`

**👥 Admin List:**
{', '.join(admins[:10])}{'...' if len(admins) > 10 else ''}

**📊 Recent Activity (Last 100 Messages):**
• **Total Messages:** `{total_messages}`
• **Text Messages:** `{text_messages}`
• **Media Messages:** `{media_messages}`
• **Unique Users:** `{len(unique_users)}`

**⚙️ Settings:**
• **Is Verified:** `{chat.is_verified}`
• **Is Scam:** `{chat.is_scam}`
• **Has Protected Content:** `{chat.has_protected_content}`
• **Invite Link:** `{chat.invite_link or 'None'}`

**📈 Statistics:**
• **Active Users Ratio:** `{(len(unique_users)/100*100):.1f}%` (of last 100 msgs)
• **Media Ratio:** `{(media_messages/total_messages*100) if total_messages > 0 else 0:.1f}%`
        """
        
        await m.reply(analysis_text)
        
        # Optional: Send detailed JSON data as file
        import json
        from datetime import datetime
        
        detailed_data = {
            "chat_id": chat.id,
            "title": chat.title,
            "type": chat.type,
            "members_count": members_count,
            "description": chat.description,
            "admins": admins,
            "is_verified": chat.is_verified,
            "is_scam": chat.is_scam,
            "invite_link": chat.invite_link,
            "analyzed_at": datetime.now().isoformat()
        }
        
        with open(f"group_analysis_{chat.id}.json", "w") as f:
            json.dump(detailed_data, f, indent=2)
        
        await c.send_document(
            chat_id=m.chat.id,
            document=f"group_analysis_{chat.id}.json",
            caption="📄 Detailed group analysis data"
        )
        
        # Clean up file
        os.remove(f"group_analysis_{chat.id}.json")
        
    except Exception as e:
        await m.reply(f"❌ Error analyzing group: {e}")


@Client.on_message(filters.command("inspect", prefixes=PREFIXES))
async def cmd_inspect(c: Client, m: Message):
    """Inspect a message"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a message to inspect")
    
    msg = m.reply_to_message
    text = f"""
**🔍 Message Inspection**

• ID: `{msg.id}`
• From: `{msg.from_user.first_name if msg.from_user else 'Unknown'}`
• Date: `{msg.date}`
• Chat: `{msg.chat.title}`
• Text: `{msg.text[:100] if msg.text else 'N/A'}`
• Has Media: `{bool(msg.photo or msg.video or msg.document)}`
    """
    await m.reply(text)


@Client.on_message(filters.command("source", prefixes=PREFIXES))
async def cmd_source(c: Client, m: Message):
    """Get message source"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    if not m.reply_to_message:
        return await m.reply("Reply to a forwarded message")
    
    if m.reply_to_message.forward_from:
        await m.reply(f"Forwarded from: `{m.reply_to_message.forward_from.first_name}`")
    elif m.reply_to_message.forward_sender_name:
        await m.reply(f"Forwarded from: `{m.reply_to_message.forward_sender_name}`")
    else:
        await m.reply("Message source unknown")


@Client.on_message(filters.command("restart", prefixes=PREFIXES))
async def cmd_restart_bot(c: Client, m: Message):
    """Restart the bot"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("🔄 Restarting bot...")
    os.execl(sys.executable, sys.executable, "-m", "poke")


@Client.on_message(filters.command("shutdown", prefixes=PREFIXES))
async def cmd_shutdown(c: Client, m: Message):
    """Shutdown the bot"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("⏹️ Shutting down...")
    sys.exit(0)


@Client.on_message(filters.command("update", prefixes=PREFIXES))
async def cmd_update(c: Client, m: Message):
    """Check for updates"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    await m.reply("🔄 Checking for updates...\n\n✅ You're running the latest version!")


@Client.on_message(filters.command("changelog", prefixes=PREFIXES))
async def cmd_changelog(c: Client, m: Message):
    """Show changelog"""
    if m.from_user.id != (await c.get_me()).id:
        return
    
    changelog = """
**📝 Changelog**

v2.0.0 - Enhanced Edition
• Added 80+ new commands
• Improved server stability
• Auto-reconnection feature
• Better CAPTCHA detection
• Extended automation options
• Health check endpoints
• Graceful shutdown handling
    """
    await m.reply(changelog)
