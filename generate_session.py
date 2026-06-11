"""
Pyrogram String Session Generator
Run this script to generate a new valid string session
"""
from pyrogram import Client
import asyncio
import os

API_ID = 12400175
API_HASH = "bd6cffecc030c99a2d23e2f9ff892c5f"

async def generate_session():
    print("🔐 Pyrogram String Session Generator\n")
    print("📱 You will receive a login code via Telegram.")
    print("   Check your Telegram app (look for message from Telegram)\n")
    
    async with Client("session_gen", api_id=API_ID, api_hash=API_HASH) as app:
        session_string = await app.export_session_string()
        
        print("\n✅ **String Session Generated Successfully!**\n")
        print("📋 Copy this session string and add it to your .env file:\n")
        print("=" * 60)
        print(f"string_session={session_string}")
        print("=" * 60)
        print("\n💡 Update your .env file with this new string_session value")
        print("   Then restart your bot.\n")

if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n\n❌ Session generation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
