import os
from dotenv import load_dotenv


load_dotenv()


API_ID: int = int(os.getenv('api_id', 0))
API_HASH: str = os.getenv('api_hash')
SESSION_STRING:str = os.getenv('string_session',None)
PREFIXES: list[str] = [".", "@", "#", "$", "%", "^", "&", "*", "~"]
BOT_USR:str = "PokeEclipseXBot"
GC_ID:int = int(os.getenv('gc_id', 0)) if os.getenv('gc_id') else 0

__all__ = [
    "API_ID",
    "API_HASH",
    "SESSION_STRING",
    "PREFIXES",
    "BOT_USR"
]