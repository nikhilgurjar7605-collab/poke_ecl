# 🎮 PokeEclipse Auto-Hunter

A Telegram userbot that automatically hunts Pokémon in @PokeEclipseXBot, tracks your PokéDollars, and handles battle responses — all hands-free.

---

## ⚠️ Before You Start

This is a userbot — it runs as your Telegram account, not a bot account.
Using userbots may violate Telegram's Terms of Service. Use at your own risk.

---

## 📋 Requirements

* Python 3.10 or higher
* A Telegram account
* Telegram API ID and API Hash
* Pyrogram session string

---

## 🛠️ Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/yourrepo/poke_ecl.git
cd poke_ecl
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Optional (recommended for speed):

```bash
pip install tgcrypto
```

### 3. Get Telegram API credentials

Go to https://my.telegram.org
Login → API Development Tools → create app
Copy api_id and api_hash

### 4. Generate session string

```python
from pyrogram import Client

with Client("my_account", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH") as app:
    print(app.export_session_string())
```

### 5. Create `.env`

```env
api_id=12345678
api_hash=abcdef1234567890abcdef1234567890
string_session=your_session_string
gc_id = your group chat id
```

---

## 🚀 Running the Bot

```bash
python -m poke
```

---

## 💬 Commands

All commands work with prefixes: `. @ # $ % ^ & * ~`

### Core Controls

| Command  | Description        |
| -------- | ------------------ |
| `.start` | Start auto-hunting |
| `.stop`  | Stop auto-hunting  |
| `.check` | Show stats         |

---

### Mode System

| Command      | Description               |
| ------------ | ------------------------- |
| `.mode pd`   | Focus on PokéDollars      |
| `.mode poke` | Focus on catching Pokémon |

---

### Pattern System

| Command      | Description                |
| ------------ | -------------------------- |
| `.pattern 1` | Only (0,0)                 |
| `.pattern 2` | (0,0), (0,1)               |
| `.pattern 3` | (0,0), (0,1), (1,0)        |
| `.pattern 4` | (0,0), (0,1), (1,0), (1,1) |

Patterns control which inline buttons are randomly clicked during battles.

---

## 🔄 How It Works

1. `.start` sends `/hunt`
2. Detects wild Pokémon messages
3. Automatically clicks battle buttons
4. Uses selected pattern for random clicks
5. Applies mode logic:

   * pd → random farming
   * poke → HP-based decisions
6. Tracks rewards and stats
7. Continues loop automatically
8. Stops if warning/captcha detected

---

## 📊 Stats Tracking

* PokéDollars earned
* Total hunts
* Pokémon caught

Check anytime using:

```bash
.check
```

---

## 📁 Project Structure

```
poke_ecl/
├── poke/
│   ├── __init__.py
│   ├── __main__.py
│   └── plugins/
│       ├── checker.py
│       ├── start.py
│       ├── mode.py
│       ├── check.py
├── config.py
├── .env
└── requirements.txt
```

---

## ⚠️ Safety

* Bot stops automatically on warnings
* Avoid long continuous runs
* Uses random delays to reduce detection

---

## ❓ Troubleshooting

TgCrypto warning
Install with `pip install tgcrypto`

Bot not responding
Make sure you sent commands from your own account

Session issues
Regenerate session string

---

## 📄 License

MIT License
