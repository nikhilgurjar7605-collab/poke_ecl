# 🎮 PokeEclipse Auto-Hunter [created by claude not by breeze]

A Telegram userbot that automatically hunts Pokémon in [@PokeEclipseXBot](https://t.me/PokeEclipseXBot), tracks your PokéDollars, and handles battle responses — all hands-free.

---

## ⚠️ Before You Start

> This is a **userbot** — it runs as *your* Telegram account, not a bot account.
> Using userbots may violate Telegram's Terms of Service. Use at your own risk.

---

## 📋 Requirements

- Python **3.10 or higher**
- A Telegram account
- Your Telegram **API ID** and **API Hash** (free, takes 2 minutes)
- A **Pyrogram session string** for your account

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

> 💡 **Optional but recommended:** Install TgCrypto for a much faster experience:
> ```bash
> pip install tgcrypto
> ```

### 3. Get your Telegram API credentials

1. Go to [https://my.telegram.org](https://my.telegram.org) and log in
2. Click **API Development Tools**
3. Fill in the form (App title and short name can be anything)
4. Copy your **api_id** and **api_hash**

### 4. Generate a session string

Run this once in your terminal to generate a session string:

```python
from pyrogram import Client

with Client("my_account", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH") as app:
    print(app.export_session_string())
```

Copy the long string it prints — that's your `string_session`.

### 5. Create your `.env` file

Create a file named `.env` in the project root folder:

```env
api_id=12345678
api_hash=abcdef1234567890abcdef1234567890
string_session=BQA...your_long_session_string_here...
```

> ⚠️ **Never share your `.env` file or session string with anyone.**
> It gives full access to your Telegram account.

---

## 🚀 Running the Bot

```bash
python -m poke
```

You should see the bot connect to Telegram. Now open your Telegram app and use the commands below.

---

## 💬 Commands

All commands can be triggered with any of these prefixes: `. @ # $ % ^ & * ~`

| Command | Description |
|---|---|
| `.start` | Start auto-hunting |
| `.stop` | Stop auto-hunting |
| `.check` | Check your current PokéDollars and total hunts |

**Example:** `.start` or `@start` or `#start` — all work the same.

---

## 🔄 How It Works

1. You send `.start` — the bot immediately sends `/hunt` to [@PokeEclipseXBot](https://t.me/PokeEclipseXBot)
2. When a wild Pokémon appears, the bot automatically clicks the battle button
3. After each hunt result (win or loss), it waits and sends `/hunt` again
4. Every 5 minutes it also sends `/hunt` on a scheduled interval as a fallback
5. If the bot receives a warning message from the game, it **automatically stops** to protect your account from a ban

---

## 📁 Project Structure

```
poke_ecl/
├── poke/
│   ├── __init__.py        # Core data and scheduler logic
│   ├── __main__.py        # Entry point
│   └── plugins/
│       ├── checker.py     # Handles bot responses and button clicks
│       ├── check.py       # The /check command
│       └── start_auto.py  # The /start and /stop commands
├── config.py              # Loads settings from .env
├── .env                   # Your credentials (you create this)
└── requirements.txt       # Python dependencies
```

---

## ❓ Troubleshooting

**`TgCrypto is missing!`**
Not an error — just a speed warning. Run `pip install tgcrypto` to fix it.

**`ValueError: invalid literal for int() with base 10: 'None'`**
Your `api_id` is missing from `.env`. Double-check the file exists and is filled in correctly.

**Bot connects but doesn't hunt**
Make sure you sent `.start` in your Telegram app *from your own account* — commands from other users are ignored.

**Session string errors / auth errors**
Your session string may be expired. Re-run the session generation script in Step 4 to get a fresh one.

---

## 📄 License

MIT — do whatever you want, but you're responsible for how you use it.