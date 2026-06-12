from pyrogram import idle
from aiohttp import web
import logging
import asyncio
import signal
import sys
import os

from poke import userbot
from config import PORT, HOST

logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_flag = False

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    global shutdown_flag
    logger.info(f"Received signal {sig}, initiating graceful shutdown...")
    shutdown_flag = True

async def web_server():
    """Simple web server to keep Render/cloud services alive"""
    app = web.Application()
    
    async def health_check(request):
        """Health check endpoint for cloud platforms"""
        status = "healthy" if not shutdown_flag else "shutting_down"
        return web.Response(text=f"Status: {status}")
    
    async def status_check(request):
        """Detailed status endpoint"""
        from .plugins import users_data, get_uptime
        return web.json_response({
            "status": "running",
            "uptime": get_uptime(),
            "in_loop": users_data["in_loop"],
            "paused": users_data.get("paused", False),
            "mode": users_data["mode"],
            "caught": users_data["poke_caught"],
            "dollars": users_data["poke_dollars"]
        })
    
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', status_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    logger.info(f"🌐 Web server started on http://{HOST}:{PORT}")
    logger.info(f"   Health check: http://{HOST}:{PORT}/health")
    logger.info(f"   Status page: http://{HOST}:{PORT}/status")
    
    # Keep running until shutdown
    while not shutdown_flag:
        await asyncio.sleep(60)
    
    await runner.cleanup()
    logger.info("Web server shut down")

async def keep_alive_monitor():
    """Monitor to ensure bot stays alive and reconnects if needed"""
    reconnect_attempts = 0
    max_reconnect_attempts = 10
    
    while not shutdown_flag:
        await asyncio.sleep(300)  # Check every 5 minutes
        
        try:
            # Check if userbot is still connected
            if not userbot.is_connected:
                logger.warning("Bot disconnected! Attempting to reconnect...")
                if reconnect_attempts < max_reconnect_attempts:
                    try:
                        userbot.start()
                        logger.info("✅ Reconnected successfully")
                        reconnect_attempts = 0
                    except Exception as e:
                        logger.error(f"Reconnection failed: {e}")
                        reconnect_attempts += 1
                else:
                    logger.error("Max reconnection attempts reached. Please restart manually.")
            else:
                logger.debug("❤️ Bot connection healthy")
        except Exception as e:
            logger.error(f"Error checking connection: {e}")

async def auto_restart_loop():
    """Auto-restart loop to keep bot running even after crashes"""
    restart_count = 0
    max_restarts = 50  # Limit to prevent infinite loops on persistent errors
    
    while not shutdown_flag:
        try:
            await asyncio.sleep(1)  # Small delay to allow normal operation
            
            # Check if bot is still connected
            if not userbot.is_connected and not shutdown_flag:
                logger.warning("⚠️ Bot connection lost! Auto-restarting in 5 seconds...")
                await asyncio.sleep(5)
                
                if restart_count < max_restarts:
                    restart_count += 1
                    logger.info(f"🔄 Auto-restart attempt {restart_count}/{max_restarts}")
                    
                    try:
                        # Stop existing session if any
                        try:
                            await userbot.stop()
                        except:
                            pass
                        
                        # Start fresh session
                        await userbot.start()
                        logger.info("✅ Bot auto-restarted successfully")
                        
                    except Exception as e:
                        logger.error(f"❌ Auto-restart failed: {e}")
                        await asyncio.sleep(10)  # Wait before next attempt
                else:
                    logger.error("Max auto-restart attempts reached. Stopping.")
                    shutdown_flag = True
                    
        except Exception as e:
            logger.error(f"Error in auto-restart loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    async def main():
        try:
            # Start the userbot
            logger.info("🤖 Starting PokeEclipse Auto-Hunter...")
            await userbot.start()
            logger.info("✅ Userbot started successfully")
            
            # Start web server for cloud platforms (keeps bot alive)
            server_task = asyncio.create_task(web_server())
            
            # Start keep-alive monitor
            monitor_task = asyncio.create_task(keep_alive_monitor())
            
            # Start auto-restart loop (immediate restart on disconnect)
            restart_task = asyncio.create_task(auto_restart_loop())
            
            logger.info("🚀 Bot is now running! Use commands to control it.")
            logger.info("🔄 Auto-restart enabled - bot will automatically recover from disconnections")
            
            # Run idle - this keeps the bot running indefinitely
            await idle()
            
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise
        finally:
            # Cleanup
            logger.info("Shutting down...")
            shutdown_flag = True
            
            # Cancel tasks
            if 'server_task' in locals():
                server_task.cancel()
            if 'monitor_task' in locals():
                monitor_task.cancel()
            if 'restart_task' in locals():
                restart_task.cancel()
            
            # Stop userbot
            try:
                await userbot.stop()
                logger.info("✅ Userbot stopped")
            except Exception as e:
                logger.error(f"Error stopping userbot: {e}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        sys.exit(1)