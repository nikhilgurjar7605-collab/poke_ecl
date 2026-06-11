# 🤖 PokeEclipse Auto-Hunter v2.0

Enhanced Edition with CAPTCHA Detection & Advanced Management Commands

## ⚠️ Disclaimer
This tool is for educational purposes only. Use at your own risk. Violating game Terms of Service may result in account bans.

## 🚀 Features

### 🎮 120+ Enhanced Commands
- **Basic Controls**: `.start`, `.stop`, `.pause`, `.resume`, `.restart`, `.autohunt`
- **Settings**: `.mode`, `.pattern`, `.run`, `.delay`, `.blacklist`, `.interval`, `.target`, `.priority`, `.smart`, `.safemode`, `.fastmode`
- **Statistics**: `.stats`, `.check`, `.history`, `.reset`, `.status`, `.export`
- **System**: `.ping`, `.uptime`, `.version`, `.settings`, `.notify`, `.autorestart`, `.info`, `.alive`, `.logs`, `.eval`
- **User**: `.me`, `.myid`, `.time`, `.date`, `.setbio`, `.setname`
- **Pokémon Game**: `.hunt`, `.catch`, `.ball`, `.bag`, `.pokemon`, `.market`, `.daily`, `.profile`, `.trade`, `.battle`
- **Group Management**: `.tagall`, `.kick`, `.ban`, `.unban`, `.mute`, `.unmute`, `.pin`, `.unpin`, `.chatinfo`, `.promote`
- **Message Actions**: `.forward`, `.copy`, `.send`, `.dm`, `.save`, `.edit`, `.reply`, `.delete`, `.clear`, `.purge`
- **Fun & Entertainment**: `.roll`, `.coin`, `.random`, `.joke`, `.quote`, `.fact`, `.compliment`, `.motivate`, `.weather`, `.love`
- **Automation**: `.remind`, `.schedule`, `.autosell`, `.autobattle`
- **Admin**: `.join`, `.leave`, `.block`, `.unblock`, `.archive`, `.unarchive`, `.whois`
- **Advanced**: `.spam`, `.fspam`, `.echo`, `.repeat`, `.type`, `.speedtest`, `.inspect`, `.source`, `.gcast`, `.gucast`
- **Bot Control**: `.update`, `.changelog`, `.shutdown`, `.restart`
- **🤖 Bot Handler (NEW)**: `.record`, `.stoprecord`, `.recordingstatus`, `.analyze`, `.setautorule`, `.toggleauto`, `.listrules`, `.clearhistory`, `.botstats`, `.exportdata`, `.importdata`


### ☁️ Cloud Deployment Features
- **Health Check Endpoints**: `/health`, `/status` - Keeps bot alive on Render/Railway/Heroku
- **Auto-Reconnection Monitor**: Automatically reconnects if connection drops
- **Graceful Shutdown**: Proper signal handling (SIGINT, SIGTERM) for clean shutdowns
- **Web Server Integration**: Built-in aiohttp server for cloud platform compatibility
- **Docker Support**: Optimized Dockerfile with health checks
- **Environment Variables**: Easy configuration via `.env` file

### Core Features
- **Auto Hunting**: Automatically hunts Pokémon and earns PokéDollars
- **Smart Battle Logic**: Attacks or catches based on HP threshold
- **Type-Based Running**: Skip specific Pokémon types
- **Multiple Modes**: Catch-focused or Dollar-focused hunting
- **Pattern Randomization**: 4 different click patterns to avoid detection

### NEW in v2.0 - Enhanced Safety
- **🛡️ CAPTCHA Detection**: Automatically detects potential CAPTCHAs and warnings
- **⏸️ Auto-Pause**: Pauses bot when CAPTCHA/warning detected
- **📬 User Notifications**: Sends alerts to your group when issues occur
- **🔒 Type Blacklist**: Block specific Pokémon types permanently
- **⏱️ Configurable Delays**: Set custom delay ranges for human-like behavior

### 🎮 20+ Management Commands

#### Basic Controls
- `.start` - Start auto hunting
- `.stop` - Stop auto hunting  
- `.pause` - Pause the bot temporarily
- `.resume` - Resume after pause/CAPTCHA
- `.restart` - Restart the bot session

#### Settings
- `.mode <poke/pd>` - Set hunting mode (catch/dollars)
- `.pattern <1-4>` - Set click pattern complexity
- `.run <type/off>` - Run from specific Pokémon type
- `.delay <min> <max>` - Set delay range (e.g., `.delay 2 5`)
- `.blacklist add/remove/list <type>` - Manage type blacklist
- `.notify <on/off>` - Toggle catch notifications
- `.autorestart` - Toggle auto-restart on captcha
- `.safemode` - Enable safe mode (3-6s delays)
- `.fastmode` - Enable fast mode (1-2s delays)

#### Statistics
- `.stats` - Show detailed session statistics
- `.check` - Quick stats check
- `.history` - Show hunt history
- `.reset` - Reset session statistics
- `.export` - Export session data to JSON

#### System
- `.ping` - Check bot response time
- `.uptime` - Show bot uptime
- `.version` - Show version info
- `.settings` - View current settings
- `.info` - Show bot and session info
- `.status` - Quick status check
- `.help` - Show all available commands
- `.features` - List all features

### 🤖 NEW: Bot Handler Commands (Interact with Other Bots)

**Recording & Analysis:**
- `.record <bot_username> [session_name]` - Start recording a bot's moves
- `.stoprecord [bot_username]` - Stop recording and save session
- `.recordingstatus` - Show all active recordings with stats
- `.analyze <filename>` - Analyze recorded data (response times, patterns, keywords)

**Auto-Response Rules:**
- `.setautorule <bot> <trigger> <response> [type]` - Set auto-response rule
  - Types: `trigger` (default), `keyword`, `timing`
  - Example: `.setautorule @PokemonBot wild pokemon catch`
- `.toggleauto <bot> <on/off>` - Enable/disable auto-responder for a bot
- `.listrules [bot]` - List all auto-response rules (optionally filter by bot)

**Data Management:**
- `.clearhistory [bot]` - Clear interaction history
- `.botstats [bot]` - Show statistics about bot interactions
- `.exportdata` - Export all bot data to JSON backup file
- `.importdata` - Import bot data from exported JSON (reply to file)

**How It Works:**
1. Start recording: `.record @PokemonBot hunting_session`
2. Interact with the bot normally - all moves are recorded
3. Stop recording: `.stoprecord @PokemonBot`
4. Analyze patterns: `.analyze PokemonBot_hunting_session_1234567890.json`
5. Set auto-rules based on analysis: `.setautorule @PokemonBot wildpokemon .catch`
6. Enable auto-responder: `.toggleauto @PokemonBot on`

The bot will now automatically respond to the target bot based on learned patterns!

## 📦 Installation

### Prerequisites
- Python 3.9+
- Telegram API credentials
- Pyrogram session string

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd poke-eclipse
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```

4. **Edit `.env` file**
```env
api_id=YOUR_API_ID
api_hash=YOUR_API_HASH
string_session=YOUR_SESSION_STRING
gc_id=YOUR_GROUP_ID
```

5. **Run the bot**
```bash
python -m poke
```

## 🚀 Deploy to Render

### Option 1: Using Procfile (Recommended)

1. Create a new **Web Service** on Render
2. Connect your GitHub repository
3. Configure build settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m poke`
4. Add environment variables in Render Dashboard:
   - `API_ID`
   - `API_HASH`
   - `STRING_SESSION`
   - `GC_ID`
5. Deploy!

### Option 2: Using Docker

1. Create a new **Web Service** on Render
2. Select **Docker** as runtime
3. Render will automatically use the `Dockerfile`
4. Add environment variables as above
5. Deploy!

### Option 3: Using render.yaml

The included `render.yaml` file provides complete configuration:

```yaml
services:
  - type: web
    name: poke-eclipse-hunter
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m poke
    envVars:
      - key: API_ID
        sync: false
      - key: API_HASH
        sync: false
      - key: STRING_SESSION
        sync: false
      - key: GC_ID
        sync: false
```

### Port Configuration

- The bot uses port **8080** by default (configurable via `PORT` env var)
- **IMPORTANT**: Render requires web services to bind to a port
- The bot now includes a lightweight HTTP server on port 8080 for health checks
- Health check endpoints: `/` and `/health`
- This keeps your Render service from sleeping

### Environment Variables for Render

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `API_ID` | Telegram API ID | Yes | - |
| `API_HASH` | Telegram API Hash | Yes | - |
| `STRING_SESSION` | Pyrogram session string | Yes | - |
| `GC_ID` | Group ID for notifications | Yes | - |
| `PORT` | Port number | No | 8080 |
| `HOST` | Host address | No | 0.0.0.0 |

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `api_id` | Telegram API ID | Yes |
| `api_hash` | Telegram API Hash | Yes |
| `string_session` | Pyrogram session string | Yes |
| `gc_id` | Group ID for notifications | Yes |

### Delay Settings
- **Safe Mode**: 3-6 seconds between actions (recommended)
- **Fast Mode**: 1-2 seconds (higher risk)
- **Custom**: Use `.delay <min> <max>` to set your own

## 🛡️ Safety Features

### CAPTCHA Detection
The bot monitors for these keywords:
- "captcha", "verify", "human"
- "click the", "select all"
- "warning", "warn", "ban"
- "suspicious", "unusual activity"

When detected:
1. Bot automatically pauses
2. Notification sent to your group
3. Wait for you to solve CAPTCHA manually
4. Use `.resume` to continue

### Warning System
- Tracks warning count
- Auto-pauses at warning threshold
- Prevents permanent ban

## 📊 Statistics Tracking

Session stats include:
- Total hunts and catch rate
- PokéDollars earned
- Runs and flees count
- Warning count
- Last catch timestamp
- Favorite Pokémon type

## 🆘 Troubleshooting

### Bot not responding?
- Check if session string is valid
- Verify API credentials
- Ensure bot is started with `.start`

### CAPTCHA detected frequently?
- Enable safe mode: `.safemode`
- Increase delays: `.delay 5 8`
- Take manual breaks

### Bot paused unexpectedly?
- Check for CAPTCHA/warning messages
- Use `.status` to see pause reason
- Solve any CAPTCHAs manually
- Use `.resume` to continue

## 📝 Command Examples

```bash
# Start hunting
.start

# Set to catch mode with pattern 3
.mode poke
.pattern 3

# Run from fire types
.run fire

# Set safe delays
.delay 3 6

# Add ghost to blacklist
.blacklist add ghost

# Check stats
.stats

# Pause for manual play
.pause

# Resume after break
.resume
```

## 🔄 Updates

### v2.0 Changes
- ✅ Added CAPTCHA detection system
- ✅ Implemented auto-pause functionality
- ✅ Added 20+ management commands
- ✅ Enhanced statistics tracking
- ✅ Type blacklist feature
- ✅ Configurable delays
- ✅ Better error handling
- ✅ User notifications

## ⚖️ Legal

This project is for educational purposes only. The developers are not responsible for any misuse or account bans. Always follow the game's Terms of Service.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

---

**Happy Hunting! 🎮**
