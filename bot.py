from telethon import TelegramClient, events
import time
from flask import Flask
from threading import Thread

# ------------------- KEEP ALIVE -------------------
app = Flask('')
@app.route('/')
def home():
    return "AFK Bot is alive ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ------------------- TELEGRAM BOT -------------------
api_id = 29604505
api_hash = '4e67360aab3a640efff67a68450bce97'
bot_token = 'YOUR_BOT_TOKEN_HERE'  # (replace with your token again if needed)

client = TelegramClient('afkbot', api_id, api_hash).start(bot_token=bot_token)

afk = False
reason = "AFK"
start_time = 0
user_custom_msg = {}
afk_private = True
afk_groups = True

# ------------------- COMMANDS -------------------
@client.on(events.NewMessage(pattern=r'^/afk(.*)'))
async def set_afk(event):
    global afk, reason, start_time
    reason = event.pattern_match.group(1).strip() or "AFK"
    afk = True
    start_time = time.time()
    await event.reply(f"🟡 I'm now AFK: {reason}")

@client.on(events.NewMessage(pattern=r'^/back'))
async def set_back(event):
    global afk
    if afk:
        afk = False
        await event.reply("🟢 I'm back online!")

# ------------------- AUTO REPLY -------------------
@client.on(events.NewMessage())
async def auto_reply(event):
    global afk, reason, start_time
    if afk:
        if (event.is_private and afk_private) or (event.is_group and afk_groups):
            user_id = event.sender_id
            if user_id not in user_custom_msg:
                elapsed = int(time.time() - start_time)
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                elapsed_str = f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"
                msg = f"⚪ I'm currently AFK: {reason} (since {elapsed_str})"
                await event.reply(msg)
                user_custom_msg[user_id] = True  # prevent spam

# ------------------- AUTO BACK WHEN YOU SEND MESSAGE -------------------
@client.on(events.NewMessage(outgoing=True))
async def auto_back(event):
    global afk
    if afk:
        afk = False
        user_custom_msg.clear()
        await event.respond("🟢 Back online automatically (message sent)!")

print("✅ AFK Bot is running...")
client.run_until_disconnected()

@client.on(events.NewMessage())
async def auto_reply(event):
    global afk, reason, start_time
    if afk:
        # Check if reply allowed in this chat type
        if (event.is_private and afk_private) or (event.is_group and afk_groups):
            # Send AFK reply to everyone, ignore dictionary for now
            elapsed = int(time.time() - start_time)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_str = f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"
            msg = f"⚪ I'm currently AFK: {reason} (since {elapsed_str})"
            await event.reply(msg)
