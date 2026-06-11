# 🤖 Bot Handler - Complete Guide

## Overview
The Bot Handler plugin allows your userbot to **record**, **analyze**, and **automatically respond** to other Telegram bots. Perfect for automating interactions with game bots, utility bots, or any automated service.

## Features

### 1. Recording Bot Moves
Capture all messages from target bots with detailed metadata:
- Message timestamps
- Text/caption content
- Reply relationships
- Keyboard/inline button data
- Media types
- Response timing

### 2. Pattern Analysis
Analyze recorded data to discover:
- Average response times
- Common commands used by the bot
- Frequently used keywords
- Interaction patterns (keyboard usage, reply behavior)
- Message type distribution

### 3. Auto-Response System
Set up intelligent auto-responses based on:
- **Trigger-based**: Respond when specific text is detected
- **Keyword-based**: Respond when keywords appear in message
- **Timing-based**: Respond at regular intervals

## Command Reference

### Recording Commands

#### `.record <bot_username> [session_name]`
Start recording all messages from a bot.

**Examples:**
```bash
.record @PokemonBot
.record @GameBot hunting_session_1
.record @TriviaBot evening_game
```

**Output:**
```
✅ Recording Started

🤖 Bot: @pokemonbot
📝 Session: hunting_session_1
⏱️ Started: 14:30:45

All messages from @pokemonbot will be recorded.
Use .stoprecord to stop recording.
```

---

#### `.stoprecord [bot_username]`
Stop recording and save the session to a JSON file.

**Examples:**
```bash
.stoprecord
.stoprecord @PokemonBot
```

**Output:**
```
✅ Recording Stopped

🤖 Bot: @pokemonbot
📊 Moves Recorded: 156
⏱️ Duration: 300.45s
💾 Saved to: recordings/pokemonbot_hunting_session_1_1718123456.json
```

---

#### `.recordingstatus`
Show all currently active recordings with statistics.

**Output:**
```
🎙️ Active Recordings

🤖 @pokemonbot
   Session: hunting_session_1
   Moves: 156
   Duration: 300.45s
   Rate: 31.16 moves/min

🤖 @gamebot
   Session: raid_battle
   Moves: 89
   Duration: 180.22s
   Rate: 29.64 moves/min
```

---

### Analysis Commands

#### `.analyze <filename>`
Analyze a recorded bot session to find patterns.

**Examples:**
```bash
.analyze
.analyze pokemonbot_hunting_session_1_1718123456.json
```

**Output:**
```
🔍 Analysis Report: pokemonbot_hunting_session_1_1718123456.json

⏱️ Response Times
   Average: 2.34s
   Min: 0.85s
   Max: 5.67s
   Samples: 155

⌨️ Top Commands
   /hunt: 45x
   /catch: 38x
   /start: 12x
   /bag: 8x
   /profile: 5x

🔑 Top Keywords
   pokemon: 67x
   wild: 45x
   caught: 38x
   appeared: 32x
   legendary: 15x
   shiny: 8x

🔄 Interaction Patterns
   Uses Keyboard: 89 (57.1%)
   Replies To Messages: 156 (100.0%)
   Sends Media: 45 (28.8%)
   Text Only: 67 (42.9%)

📊 Total Moves Analyzed: 156
💾 Full analysis saved to: analysis/analysis_pokemonbot_hunting_session_1_1718123456_1718123789.json
```

---

### Auto-Response Commands

#### `.setautorule <bot> <trigger> <response> [rule_type]`
Create an auto-response rule for a bot.

**Rule Types:**
- `trigger` (default): Respond when exact trigger text is found
- `keyword`: Respond when any keyword appears
- `timing`: Respond after specified delay in seconds

**Examples:**
```bash
# Trigger-based
.setautorule @PokemonBot wild pokemon .catch
.setautorule @PokemonBot appeared useball

# Keyword-based
.setautorule @GameBot start Let's play! keyword

# Timing-based (respond every 30 seconds)
.setautorule @IdleBot 30 .collect timing
```

**Output:**
```
✅ Auto-Response Rule Added

🤖 Bot: @pokemonbot
🎯 Trigger: wild pokemon
💬 Response: .catch
📋 Type: trigger

Enable with: .toggleauto @pokemonbot on
```

---

#### `.toggleauto <bot_username> <on|off>`
Enable or disable auto-responder for a bot.

**Examples:**
```bash
.toggleauto @PokemonBot on
.toggleauto @GameBot off
```

**Output:**
```
✅ Auto-responder ENABLED for @pokemonbot
```

---

#### `.listrules [bot_username]`
List all configured auto-response rules.

**Examples:**
```bash
.listrules
.listrules @PokemonBot
```

**Output:**
```
📜 Auto-Response Rules

🤖 @pokemonbot
   Triggers:
      wild pokemon → .catch
      appeared → useball
      legendary → .ultraball
   Patterns:
      Keywords: ['shiny', 'rare'] → .masterball
      Every 30.0s → .collect

🤖 @gamebot
   Triggers:
      start → Let's play!
```

---

### Data Management Commands

#### `.clearhistory [bot_username]`
Clear stored interaction history for a bot.

**Examples:**
```bash
.clearhistory
.clearhistory @PokemonBot
```

---

#### `.botstats [bot_username]`
Show statistics about bot interactions.

**Examples:**
```bash
.botstats
.botstats @PokemonBot
```

**Output:**
```
📊 Stats for @pokemonbot

Total Interactions: 1250

Message Types:
   text: 890
   media: 360

Time Range: 45.3 minutes
```

---

#### `.exportdata`
Export all bot data (recordings, rules, history) to a JSON backup file.

**Output:**
```
✅ Data Exported

📦 File: bot_export_1718123456.json
📊 Recordings: 5
🤖 Bots with rules: 3
📝 History entries: 2450

Download this file to backup your bot data!
```

---

#### `.importdata`
Import bot data from an exported JSON file (reply to the file).

**Usage:**
1. Send the exported JSON file to your chat
2. Reply to the file with `.importdata`

**Output:**
```
✅ Data Imported Successfully

📦 Bots with rules: 3
💾 Data merged with existing data
```

---

## Complete Workflow Example

### Scenario: Automate Pokémon Bot Hunting

**Step 1: Start Recording**
```bash
.record @PokemonBot morning_hunt
```

**Step 2: Play Normally**
Interact with @PokemonBot as you normally would:
- Send `/hunt`
- Wait for Pokémon to appear
- Send `.catch`
- Continue hunting for 5-10 minutes

**Step 3: Stop Recording**
```bash
.stoprecord @PokemonBot
```

**Step 4: Analyze Patterns**
```bash
.analyze PokemonBot_morning_hunt_1718123456.json
```

Review the analysis to understand:
- How often "wild" appears before catches
- Response time patterns
- Common keywords

**Step 5: Set Auto-Rules**
Based on analysis, create rules:
```bash
.setautorule @PokemonBot wild .catch
.setautorule @PokemonBot appeared .useball
.setautorule @PokemonBot legendary .masterball
```

**Step 6: Enable Auto-Responder**
```bash
.toggleauto @PokemonBot on
```

**Step 7: Monitor**
Check stats periodically:
```bash
.botstats @PokemonBot
.recordingstatus
```

---

## Storage Structure

```
/workspace/
├── recordings/           # Saved bot session recordings
│   ├── pokemonbot_session1_1718123456.json
│   └── gamebot_raid_1718124567.json
├── analysis/             # Generated analysis reports
│   ├── analysis_pokemonbot_session1_1718123456_1718123789.json
│   └── analysis_gamebot_raid_1718124567_1718125678.json
└── bot_export_*.json     # Exported backups
```

## Advanced Tips

### 1. Multiple Sessions
Record different sessions for different times of day:
```bash
.record @PokemonBot morning_session
.record @PokemonBot evening_session
.record @PokemonBot night_session
```

### 2. Pattern Refinement
Analyze multiple sessions to find consistent patterns:
```bash
.analyze pokemonbot_morning_*.json
.analyze pokemonbot_evening_*.json
```

### 3. Backup Regularly
Export your configuration regularly:
```bash
.exportdata
```

### 4. Test Rules Incrementally
Start with simple rules, then add complexity:
```bash
# Start simple
.setautorule @PokemonBot wild .catch

# Add more specific rules
.setautorule @PokemonBot legendary .masterball
.setautorule @PokemonBot shiny .ultraball
```

## Troubleshooting

### Recording Not Starting
- Ensure bot username is correct (with or without @)
- Check if bot is in a chat you both share
- Verify you have permission to send messages

### Auto-Response Not Working
- Check if auto-responder is enabled: `.toggleauto @bot on`
- Verify rules exist: `.listrules @bot`
- Ensure trigger text matches exactly (case-insensitive)

### Analysis Shows No Data
- Make sure you stopped the recording properly
- Check that enough messages were recorded (minimum 2 for analysis)
- Verify the recording file exists in `recordings/` directory

## Security Notes

⚠️ **Important:**
- Bot data is stored locally on your server
- Export files contain all interaction history - keep them secure
- Auto-responses can be detected by game anti-bot systems
- Use reasonable delays to avoid detection
- Always comply with Telegram's Terms of Service

---

**Total Commands Added:** 11 new bot handler commands
**Plugin File:** `poke/plugins/bot_handler.py` (675 lines)
