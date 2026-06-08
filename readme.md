# PokeEclipse Auto-Hunter

Telegram userbot that auto-hunts Pokémon in @PokeEclipseXBot — battles, catches, and tracks stats hands-free.

> **Warning:** Runs as your Telegram account. May violate Telegram's ToS. Use at your own risk.

---

## Setup

**1. Clone & install**
```bash
git clone https://github.com/yourrepo/poke_ecl.git
cd poke_ecl
pip install -r requirements.txt
```

**2. Get credentials** — [my.telegram.org](https://my.telegram.org) → API Development Tools → Create app

**3. Generate session string**
```python
from pyrogram import Client
with Client("acc", api_id=YOUR_ID, api_hash="YOUR_HASH") as app:
    print(app.export_session_string())
```

**4. Create `.env`**
```env
api_id=12345678
api_hash=your_api_hash
string_session=your_session_string
gc_id=your_group_chat_id
```

**5. Run**
```bash
python -m poke
```

---

## Commands

Prefixes: `. @ # $ % ^ & * ~`

| Command       | Description                              |
| ------------- | ---------------------------------------- |
| `.start`      | Start auto-hunting                       |
| `.stop`       | Stop auto-hunting                        |
| `.check`      | Show stats                               |
| `.mode pd`    | Farm PokéDollars                         |
| `.mode poke`  | Catch Pokémon (HP-based)                 |
| `.pattern 1–4`| Set which battle buttons to click        |
| `.run <type>` | Auto-run from that Pokémon type          |
| `.run off`    | Disable auto-run                         |
| `.run off`    | same as readme but short                 |
---

## Notes

- Auto-stops on captcha or warning detection
- Uses random delays to avoid detection
- Stats tracked: hunts, catches, PokéDollars

---

## License

MIT