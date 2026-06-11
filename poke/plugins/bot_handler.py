"""
Bot Handler Plugin - Interact with, record, and analyze other bots
Records moves, analyzes patterns, and automates responses based on learned behavior
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from poke import app
import asyncio
import json
import time
import re
from collections import defaultdict, Counter
from datetime import datetime
import os

# Storage paths
RECORDINGS_DIR = "recordings"
ANALYSIS_DIR = "analysis"

# Ensure directories exist
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# In-memory storage for active recordings
active_recordings = {}
bot_patterns = defaultdict(list)
auto_responses = {}
move_history = defaultdict(list)

class MoveRecorder:
    """Records and stores bot moves for analysis"""
    
    def __init__(self, bot_username: str, session_name: str):
        self.bot_username = bot_username.lower().strip('@')
        self.session_name = session_name
        self.moves = []
        self.start_time = time.time()
        self.is_recording = True
        
    def add_move(self, message: Message):
        """Record a move from the bot"""
        move_data = {
            'timestamp': time.time(),
            'message_id': message.id,
            'text': message.text,
            'caption': message.caption,
            'reply_to': message.reply_to_message.id if message.reply_to_message else None,
            'has_keyboard': bool(message.reply_markup),
            'keyboard_data': str(message.reply_markup) if message.reply_markup else None,
            'media_type': message.media.value if message.media else None,
            'from_user': message.from_user.username if message.from_user else None,
        }
        self.moves.append(move_data)
        
    def get_stats(self):
        """Get recording statistics"""
        duration = time.time() - self.start_time
        return {
            'bot': self.bot_username,
            'session': self.session_name,
            'moves_recorded': len(self.moves),
            'duration_seconds': round(duration, 2),
            'moves_per_minute': round(len(self.moves) / (duration / 60), 2) if duration > 0 else 0
        }
    
    def save(self):
        """Save recording to file"""
        filename = f"{RECORDINGS_DIR}/{self.bot_username}_{self.session_name}_{int(time.time())}.json"
        data = {
            'bot_username': self.bot_username,
            'session_name': self.session_name,
            'start_time': self.start_time,
            'end_time': time.time(),
            'total_moves': len(self.moves),
            'moves': self.moves
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename

class PatternAnalyzer:
    """Analyzes recorded bot moves to find patterns"""
    
    def __init__(self, recording_file: str = None, moves: list = None):
        self.moves = moves or []
        if recording_file:
            self.load_from_file(recording_file)
            
    def load_from_file(self, filename: str):
        """Load moves from a recording file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.moves = data.get('moves', [])
    
    def analyze_response_times(self):
        """Analyze how fast the bot responds"""
        if len(self.moves) < 2:
            return {'error': 'Not enough moves'}
        
        response_times = []
        for i in range(1, len(self.moves)):
            time_diff = self.moves[i]['timestamp'] - self.moves[i-1]['timestamp']
            response_times.append(time_diff)
        
        return {
            'average_response_time': sum(response_times) / len(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'total_samples': len(response_times)
        }
    
    def analyze_command_patterns(self):
        """Find common commands or triggers"""
        commands = []
        for move in self.moves:
            text = move.get('text') or move.get('caption') or ''
            if text.startswith('/'):
                cmd = text.split()[0].lower()
                commands.append(cmd)
        
        return Counter(commands).most_common(10)
    
    def analyze_keyword_patterns(self):
        """Find common keywords in bot responses"""
        keywords = []
        common_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being']
        
        for move in self.moves:
            text = (move.get('text') or move.get('caption') or '').lower()
            words = re.findall(r'\b[a-z]{3,}\b', text)
            for word in words:
                if word not in common_words:
                    keywords.append(word)
        
        return Counter(keywords).most_common(20)
    
    def analyze_interaction_patterns(self):
        """Analyze how the bot interacts (replies, keyboards, etc.)"""
        patterns = {
            'uses_keyboard': 0,
            'replies_to_messages': 0,
            'sends_media': 0,
            'text_only': 0
        }
        
        for move in self.moves:
            if move.get('has_keyboard'):
                patterns['uses_keyboard'] += 1
            if move.get('reply_to'):
                patterns['replies_to_messages'] += 1
            if move.get('media_type'):
                patterns['sends_media'] += 1
            if not move.get('media_type') and not move.get('has_keyboard'):
                patterns['text_only'] += 1
        
        total = len(self.moves)
        return {k: f"{v} ({round(v/total*100, 1)}%)" if total > 0 else 0 for k, v in patterns.items()}
    
    def generate_full_analysis(self):
        """Generate comprehensive analysis report"""
        return {
            'response_times': self.analyze_response_times(),
            'command_patterns': self.analyze_command_patterns(),
            'keyword_patterns': self.analyze_keyword_patterns(),
            'interaction_patterns': self.analyze_interaction_patterns(),
            'total_moves_analyzed': len(self.moves)
        }

class AutoResponder:
    """Automatically responds to bots based on learned patterns"""
    
    def __init__(self, bot_username: str, rules: dict):
        self.bot_username = bot_username.lower().strip('@')
        self.rules = rules
        self.is_active = False
        self.last_response = {}
        
    def should_respond(self, message: Message) -> tuple[bool, str]:
        """Check if we should respond to this message"""
        if not self.is_active:
            return False, None
            
        text = (message.text or message.caption or '').lower()
        
        # Check trigger-based rules
        if 'triggers' in self.rules:
            for trigger, response in self.rules['triggers'].items():
                if trigger.lower() in text:
                    return True, response
        
        # Check pattern-based rules
        if 'patterns' in self.rules:
            for pattern_config in self.rules['patterns']:
                if pattern_config.get('type') == 'keyword':
                    keywords = pattern_config.get('keywords', [])
                    if any(kw.lower() in text for kw in keywords):
                        responses = pattern_config.get('responses', [])
                        if responses:
                            return True, responses[0]  # Could be randomized
                
                elif pattern_config.get('type') == 'timing':
                    # Respond after certain time delay
                    last_time = self.last_response.get(message.chat.id, 0)
                    min_delay = pattern_config.get('min_delay', 0)
                    if time.time() - last_time >= min_delay:
                        return True, pattern_config.get('response', '')
        
        return False, None
    
    def execute_response(self, chat_id: int, response: str):
        """Execute the response (to be called by main handler)"""
        self.last_response[chat_id] = time.time()
        return response

# Command Handlers

@app.on_message(filters.command("record", prefixes=".") & filters.me)
async def start_recording(client: Client, message: Message):
    """Start recording a bot's moves"""
    args = message.text.split(maxsplit=2)
    
    if len(args) < 2:
        await message.edit("Usage: `.record <bot_username> [session_name]`\n\nExample: `.record @PokemonBot hunt_session`")
        return
    
    bot_username = args[1]
    session_name = args[2] if len(args) > 2 else f"session_{int(time.time())}"
    
    bot_username_clean = bot_username.lower().strip('@')
    
    # Start recording
    recorder = MoveRecorder(bot_username_clean, session_name)
    active_recordings[bot_username_clean] = recorder
    
    await message.edit(
        f"✅ **Recording Started**\n\n"
        f"🤖 Bot: @{bot_username_clean}\n"
        f"📝 Session: `{session_name}`\n"
        f"⏱️ Started: {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"All messages from @{bot_username_clean} will be recorded.\n"
        f"Use `.stoprecord` to stop recording."
    )

@app.on_message(filters.command("stoprecord", prefixes=".") & filters.me)
async def stop_recording(client: Client, message: Message):
    """Stop recording and save the session"""
    args = message.text.split(maxsplit=1)
    bot_username = args[1].strip('@').lower() if len(args) > 1 else None
    
    if not bot_username:
        # Stop all recordings
        if not active_recordings:
            await message.edit("❌ No active recordings found.")
            return
        
        stopped = []
        for bot, recorder in active_recordings.items():
            filename = recorder.save()
            stats = recorder.get_stats()
            stopped.append(f"• @{bot}: {stats['moves_recorded']} moves saved to `{filename}`")
            del active_recordings[bot]
        
        await message.edit(
            f"✅ **Stopped All Recordings**\n\n" + 
            "\n".join(stopped)
        )
    else:
        if bot_username not in active_recordings:
            await message.edit(f"❌ No active recording for @{bot_username}")
            return
        
        recorder = active_recordings[bot_username]
        filename = recorder.save()
        stats = recorder.get_stats()
        
        del active_recordings[bot_username]
        
        await message.edit(
            f"✅ **Recording Stopped**\n\n"
            f"🤖 Bot: @{bot_username}\n"
            f"📊 Moves Recorded: `{stats['moves_recorded']}`\n"
            f"⏱️ Duration: `{stats['duration_seconds']}s`\n"
            f"💾 Saved to: `{filename}`"
        )

@app.on_message(filters.command("recordingstatus", prefixes=".") & filters.me)
async def recording_status(client: Client, message: Message):
    """Show status of active recordings"""
    if not active_recordings:
        await message.edit("📴 No active recordings.")
        return
    
    status_msg = "🎙️ **Active Recordings**\n\n"
    for bot, recorder in active_recordings.items():
        stats = recorder.get_stats()
        status_msg += (
            f"🤖 @{bot}\n"
            f"   Session: `{recorder.session_name}`\n"
            f"   Moves: `{stats['moves_recorded']}`\n"
            f"   Duration: `{stats['duration_seconds']}s`\n"
            f"   Rate: `{stats['moves_per_minute']}` moves/min\n\n"
        )
    
    await message.edit(status_msg)

@app.on_message(filters.command("analyze", prefixes=".") & filters.me)
async def analyze_recording(client: Client, message: Message):
    """Analyze a recorded bot session"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        # List available recordings
        files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith('.json')]
        if not files:
            await message.edit("📁 No recordings found. Start recording with `.record <bot>`")
            return
        
        file_list = "\n".join([f"• `{f}`" for f in sorted(files)[-10:]])  # Last 10
        await message.edit(
            f"📂 **Available Recordings** (last 10)\n\n{file_list}\n\n"
            f"Use: `.analyze <filename>` to analyze a specific recording"
        )
        return
    
    filename = args[1]
    filepath = os.path.join(RECORDINGS_DIR, filename)
    
    if not os.path.exists(filepath):
        # Try without directory
        filepath = os.path.join(RECORDINGS_DIR, f"{filename}.json")
        if not os.path.exists(filepath):
            await message.edit(f"❌ Recording not found: `{filename}`")
            return
    
    analyzer = PatternAnalyzer(filepath)
    analysis = analyzer.generate_full_analysis()
    
    # Format response
    response = f"🔍 **Analysis Report**: `{filename}`\n\n"
    
    # Response times
    rt = analysis['response_times']
    if 'error' not in rt:
        response += (
            f"⏱️ **Response Times**\n"
            f"   Average: `{rt['average_response_time']:.2f}s`\n"
            f"   Min: `{rt['min_response_time']:.2f}s`\n"
            f"   Max: `{rt['max_response_time']:.2f}s`\n"
            f"   Samples: `{rt['total_samples']}`\n\n"
        )
    
    # Command patterns
    if analysis['command_patterns']:
        response += "⌨️ **Top Commands**\n"
        for cmd, count in analysis['command_patterns'][:5]:
            response += f"   `{cmd}`: {count}x\n"
        response += "\n"
    
    # Keyword patterns
    if analysis['keyword_patterns']:
        response += "🔑 **Top Keywords**\n"
        for keyword, count in analysis['keyword_patterns'][:10]:
            response += f"   `{keyword}`: {count}x\n"
        response += "\n"
    
    # Interaction patterns
    response += "🔄 **Interaction Patterns**\n"
    for pattern, value in analysis['interaction_patterns'].items():
        response += f"   {pattern.replace('_', ' ').title()}: `{value}`\n"
    
    response += f"\n📊 Total Moves Analyzed: `{analysis['total_moves_analyzed']}`"
    
    # Save analysis
    analysis_file = f"{ANALYSIS_DIR}/analysis_{filename.replace('.json', '')}_{int(time.time())}.json"
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    response += f"\n💾 Full analysis saved to: `{analysis_file}`"
    
    await message.edit(response)

@app.on_message(filters.command("setautorule", prefixes=".") & filters.me)
async def set_auto_rule(client: Client, message: Message):
    """Set an auto-response rule for a bot"""
    args = message.text.split(maxsplit=4)
    
    if len(args) < 5:
        await message.edit(
            "Usage: `.setautorule <bot> <trigger> <response> [rule_type]`\n\n"
            "Examples:\n"
            "`.setautorule @PokemonBot wild pokemon catch`\n"
            "`.setautorule @GameBot start Let's play!`\n\n"
            "Rule types: `trigger` (default), `keyword`, `timing`"
        )
        return
    
    bot_username = args[1].strip('@').lower()
    trigger = args[2]
    response = args[3]
    rule_type = args[4] if len(args) > 4 else 'trigger'
    
    if bot_username not in auto_responses:
        auto_responses[bot_username] = {'triggers': {}, 'patterns': []}
    
    if rule_type == 'trigger':
        auto_responses[bot_username]['triggers'][trigger] = response
    elif rule_type == 'keyword':
        auto_responses[bot_username]['patterns'].append({
            'type': 'keyword',
            'keywords': [trigger],
            'responses': [response]
        })
    elif rule_type == 'timing':
        try:
            delay = float(trigger)
            auto_responses[bot_username]['patterns'].append({
                'type': 'timing',
                'min_delay': delay,
                'response': response
            })
        except ValueError:
            await message.edit("❌ For timing rules, trigger must be a number (seconds)")
            return
    
    await message.edit(
        f"✅ **Auto-Response Rule Added**\n\n"
        f"🤖 Bot: @{bot_username}\n"
        f"🎯 Trigger: `{trigger}`\n"
        f"💬 Response: `{response}`\n"
        f"📋 Type: `{rule_type}`\n\n"
        f"Enable with: `.toggleauto @{bot_username} on`"
    )

@app.on_message(filters.command("toggleauto", prefixes=".") & filters.me)
async def toggle_auto_responder(client: Client, message: Message):
    """Toggle auto-responder for a bot"""
    args = message.text.split(maxsplit=2)
    
    if len(args) < 3:
        await message.edit("Usage: `.toggleauto <bot_username> <on|off>`")
        return
    
    bot_username = args[1].strip('@').lower()
    state = args[2].lower()
    
    if bot_username not in auto_responses or not auto_responses[bot_username]:
        await message.edit(f"❌ No rules set for @{bot_username}. Use `.setautorule` first.")
        return
    
    if state in ['on', 'enable', 'true', '1']:
        # Create responder if not exists
        if bot_username not in globals().get('_responders', {}):
            if '_responders' not in globals():
                global _responders
                _responders = {}
            _responders[bot_username] = AutoResponder(bot_username, auto_responses[bot_username])
        
        _responders[bot_username].is_active = True
        await message.edit(f"✅ Auto-responder **ENABLED** for @{bot_username}")
    else:
        if '_responders' in globals() and bot_username in _responders:
            _responders[bot_username].is_active = False
        await message.edit(f"🚫 Auto-responder **DISABLED** for @{bot_username}")

@app.on_message(filters.command("listrules", prefixes=".") & filters.me)
async def list_rules(client: Client, message: Message):
    """List all auto-response rules"""
    args = message.text.split(maxsplit=1)
    bot_filter = args[1].strip('@').lower() if len(args) > 1 else None
    
    if not auto_responses:
        await message.edit("📭 No auto-response rules set.")
        return
    
    response = "📜 **Auto-Response Rules**\n\n"
    
    for bot, rules in auto_responses.items():
        if bot_filter and bot != bot_filter:
            continue
        
        response += f"🤖 **@{bot}**\n"
        
        if rules.get('triggers'):
            response += "   Triggers:\n"
            for trigger, resp in list(rules['triggers'].items())[:5]:
                response += f"      `{trigger}` → `{resp[:30]}...`\n" if len(resp) > 30 else f"      `{trigger}` → `{resp}`\n"
        
        if rules.get('patterns'):
            response += "   Patterns:\n"
            for pattern in rules['patterns'][:3]:
                if pattern['type'] == 'keyword':
                    response += f"      Keywords: {pattern['keywords']} → `{pattern['responses'][0][:30]}...`\n"
                elif pattern['type'] == 'timing':
                    response += f"      Every {pattern['min_delay']}s → `{pattern['response'][:30]}...`\n"
        
        response += "\n"
    
    if bot_filter and len(response.strip()) == len("📜 **Auto-Response Rules**\n\n"):
        await message.edit(f"❌ No rules found for @{bot_filter}")
    else:
        await message.edit(response)

@app.on_message(filters.command("clearhistory", prefixes=".") & filters.me)
async def clear_history(client: Client, message: Message):
    """Clear move history for a bot"""
    args = message.text.split(maxsplit=1)
    bot_username = args[1].strip('@').lower() if len(args) > 1 else None
    
    if bot_username:
        if bot_username in move_history:
            del move_history[bot_username]
            await message.edit(f"🗑️ Cleared history for @{bot_username}")
        else:
            await message.edit(f"ℹ️ No history found for @{bot_username}")
    else:
        move_history.clear()
        await message.edit("🗑️ Cleared all bot histories")

@app.on_message(filters.command("botstats", prefixes=".") & filters.me)
async def bot_stats(client: Client, message: Message):
    """Show statistics about bot interactions"""
    args = message.text.split(maxsplit=1)
    bot_username = args[1].strip('@').lower() if len(args) > 1 else None
    
    if bot_username:
        history = move_history.get(bot_username, [])
        if not history:
            await message.edit(f"📊 No interaction history for @{bot_username}")
            return
        
        response = f"📊 **Stats for @{bot_username}**\n\n"
        response += f"Total Interactions: `{len(history)}`\n"
        
        # Count message types
        types = Counter(h.get('type', 'unknown') for h in history)
        response += "\nMessage Types:\n"
        for msg_type, count in types.most_common():
            response += f"   {msg_type}: `{count}`\n"
        
        # Time range
        if history:
            times = [h.get('timestamp', 0) for h in history]
            duration = max(times) - min(times)
            response += f"\nTime Range: `{duration/60:.1f}` minutes\n"
        
        await message.edit(response)
    else:
        # Show summary for all bots
        total = sum(len(h) for h in move_history.values())
        response = f"📊 **Overall Bot Stats**\n\n"
        response += f"Total Bots Tracked: `{len(move_history)} `\n"
        response += f"Total Interactions: `{total}`\n\n"
        
        for bot, history in list(move_history.items())[:5]:
            response += f"• @{bot}: `{len(history)}` interactions\n"
        
        await message.edit(response)

@app.on_message(filters.command("exportdata", prefixes=".") & filters.me)
async def export_data(client: Client, message: Message):
    """Export all bot data to a JSON file"""
    export_data = {
        'timestamp': time.time(),
        'recordings': {},
        'auto_responses': auto_responses,
        'move_history': dict(move_history),
        'active_recordings': {k: v.get_stats() for k, v in active_recordings.items()}
    }
    
    # Load all recording files
    for filename in os.listdir(RECORDINGS_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(RECORDINGS_DIR, filename)
            with open(filepath, 'r') as f:
                export_data['recordings'][filename] = json.load(f)
    
    export_file = f"bot_export_{int(time.time())}.json"
    with open(export_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    await message.edit(
        f"✅ **Data Exported**\n\n"
        f"📦 File: `{export_file}`\n"
        f"📊 Recordings: `{len(export_data['recordings'])}`\n"
        f"🤖 Bots with rules: `{len(auto_responses)}`\n"
        f"📝 History entries: `{sum(len(h) for h in move_history.values())}`\n\n"
        f"Download this file to backup your bot data!"
    )

@app.on_message(filters.command("importdata", prefixes=".") & filters.me)
async def import_data(client: Client, message: Message):
    """Import bot data from a JSON file (reply to file)"""
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.edit("Reply to a bot export JSON file with `.importdata`")
        return
    
    doc = message.reply_to_message.document
    if not doc.file_name.endswith('.json'):
        await message.edit("❌ Please reply to a JSON file")
        return
    
    await message.edit("⏳ Downloading and importing data...")
    
    file_path = await client.download_media(message.reply_to_message)
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        imported_count = 0
        
        # Import auto-responses
        if 'auto_responses' in data:
            auto_responses.update(data['auto_responses'])
            imported_count += len(data['auto_responses'])
        
        # Import move history
        if 'move_history' in data:
            for bot, history in data['move_history'].items():
                move_history[bot].extend(history)
            imported_count += len(data['move_history'])
        
        await message.edit(
            f"✅ **Data Imported Successfully**\n\n"
            f"📦 Bots with rules: `{imported_count}`\n"
            f"💾 Data merged with existing data"
        )
    except Exception as e:
        await message.edit(f"❌ Import failed: `{str(e)}`")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Listener to capture bot messages during recording
@app.on_message(~filters.me & ~filters.bot)
async def capture_bot_messages(client: Client, message: Message):
    """Capture messages from bots being recorded"""
    if not message.from_user or not message.from_user.is_bot:
        return
    
    bot_username = message.from_user.username
    if not bot_username:
        return
    
    bot_username = bot_username.lower()
    
    # Record if actively recording
    if bot_username in active_recordings:
        active_recordings[bot_username].add_move(message)
    
    # Add to history
    move_history[bot_username].append({
        'timestamp': time.time(),
        'message_id': message.id,
        'text': message.text,
        'type': 'text' if message.text else ('media' if message.media else 'other')
    })
    
    # Keep history manageable (last 1000 messages per bot)
    if len(move_history[bot_username]) > 1000:
        move_history[bot_username] = move_history[bot_username][-1000:]
    
    # Check auto-responder
    if '_responders' in globals() and bot_username in _responders:
        responder = _responders[bot_username]
        should_respond, response_text = responder.should_respond(message)
        
        if should_respond and response_text:
            await asyncio.sleep(1)  # Small delay to seem natural
            try:
                await message.reply(response_text)
            except Exception as e:
                print(f"Auto-response failed: {e}")
