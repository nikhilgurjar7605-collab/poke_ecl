# 🔧 Userbot Not Responding - Troubleshooting Guide

## Issue: Bot is not responding to commands

### Root Cause Identified
The error `AUTH_KEY_UNREGISTERED` means your string session is invalid or expired. This happens when:
1. The session was generated on a different device/IP
2. Telegram invalidated the session for security
3. The session file was corrupted

---

## ✅ Solution: Generate New Session

### Option 1: Run the Session Generator (Recommended)

```bash
python generate_session.py
```

Follow these steps:
1. Run the script above
2. Enter your phone number when prompted (with country code, e.g., +1234567890)
3. Check your Telegram app for the login code
4. Enter the code in the terminal
5. If you have 2FA enabled, enter your password
6. Copy the generated `string_session` value
7. Update your `.env` file with the new session

### Option 2: Manual .env Update

Edit `/workspace/.env` and replace the `string_session` value:

```env
api_id=12400175
api_hash=bd6cffecc030c99a2d23e2f9ff892c5f
string_session=YOUR_NEW_SESSION_HERE
gc_id=-1004294472272
```

---

## 🚀 Start the Bot

After updating the session:

```bash
python -m poke
```

You should see:
```
🤖 Starting PokeEclipse Auto-Hunter...
✅ Userbot started successfully
🌐 Web server started on http://0.0.0.0:8080
🚀 Bot is now running! Use commands to control it.
```

---

## 📝 Test Commands

Once running, send these commands to your bot on Telegram:
- `.help` - Show all commands
- `.ping` - Check response time
- `.status` - Quick status check
- `.alive` - Check if bot is alive

---

## ⚠️ Common Issues

### "Missing API_ID or API_HASH"
Make sure your `.env` file has valid credentials from https://my.telegram.org/apps

### "Phone number is required"
Run the session generator again and complete the full login process

### Bot starts but doesn't respond to commands
1. Make sure you're using the correct prefix (`.` by default)
2. Commands only work when sent from YOUR account (the one in the session)
3. Check that plugins are loading correctly

---

## 📂 File Locations

- Config: `/workspace/config.py`
- Environment: `/workspace/.env`
- Main entry: `/workspace/poke/__main__.py`
- Plugins: `/workspace/poke/plugins/`

---

## 🆘 Still Having Issues?

1. Delete any existing session files:
   ```bash
   rm -f poke_ecl.session session_gen.session
   ```

2. Regenerate the string session:
   ```bash
   python generate_session.py
   ```

3. Restart the bot:
   ```bash
   python -m poke
   ```
