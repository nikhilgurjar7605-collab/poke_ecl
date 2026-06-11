import os
from dotenv import load_dotenv


load_dotenv()


# Validate required credentials
API_ID_raw = os.getenv('api_id')
API_HASH = os.getenv('api_hash')
SESSION_STRING = os.getenv('string_session', None)

if not API_ID_raw or not API_HASH:
    print("❌ ERROR: Missing required credentials!")
    print("Please set the following environment variables:")
    print("  - api_id: Get from https://my.telegram.org/apps")
    print("  - api_hash: Get from https://my.telegram.org/apps")
    print("\nYou can set them in a .env file or as environment variables.")
    raise ValueError("Missing API_ID or API_HASH")

API_ID: int = int(API_ID_raw)
PREFIXES: list[str] = [".", "@", "#", "$", "%", "^", "&", "*", "~"]
BOT_USR:str = "PokeEclipseXBot"

# GC_ID is optional for some features
GC_ID_raw = os.getenv('gc_id', '0')
try:
    GC_ID: int = int(GC_ID_raw)
except ValueError:
    GC_ID = 0

# Render/Cloud Deployment Support
PORT: int = int(os.getenv('PORT', 8080))
HOST: str = os.getenv('HOST', '0.0.0.0')

__all__ = [
    "API_ID",
    "API_HASH",
    "SESSION_STRING",
    "PREFIXES",
    "BOT_USR",
    "GC_ID",
    "PORT",
    "HOST"
]