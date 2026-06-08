from pyrogram import idle
from aiohttp import web
import logging

from poke import userbot
from config import PORT, HOST

logger = logging.getLogger(__name__)

async def web_server():
    """Simple web server to keep Render alive"""
    app = web.Application()
    
    async def health_check(request):
        return web.Response(text="OK")
    
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    logger.info(f"Web server started on http://{HOST}:{PORT}")
    
    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Start the bot
        userbot.start()
        
        # Start web server for Render
        server_task = asyncio.create_task(web_server())
        
        # Run idle
        await idle()
        
        # Cleanup
        server_task.cancel()
        userbot.stop()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")