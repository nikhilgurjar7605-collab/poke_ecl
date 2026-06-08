import os
from dotenv import load_dotenv


load_dotenv()


API_ID: int = int(os.getenv('api_id'))
API_HASH: str = os.getenv('api_hash')
SESSION_STRING:str = os.getenv('string_session',None)
PREFIXES: list[str] = [".", "@", "#", "$", "%", "^", "&", "*", "~"]
BOT_USR:str = "PokeEclipseXBot"
GC_ID:int = int(os.getenv('gc_id'))

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