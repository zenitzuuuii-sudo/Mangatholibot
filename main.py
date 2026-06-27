from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import os
from welcome import on_member_join as handle_welcome

# ---------------- KEEP ALIVE SERVER ---------------- #

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

# ---------------- DISCORD BOT ---------------- #

TOKEN = os.getenv("DISCORD_TOKEN")

USER_MESSAGES = {
    1445755328783192096: "𝗪𝗛𝗔𝗧'𝗦 𝗧𝗛𝗘 𝗠𝗔𝗧𝗧𝗘𝗥, 𝗗𝗔𝗥𝗟𝗜𝗡𝗚?",
    1512533353088155731: "𝗜'𝗠 𝗚𝗔𝗬",
    1377245405636460575: "𝗦𝗧𝗜𝗖𝗞 𝗜𝗦 𝗛𝗘𝗥!"
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- EVENTS ---------------- #

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for member in message.mentions:
        if member.id in USER_MESSAGES:
            await message.channel.send(
                f"{member.mention}\n# {USER_MESSAGES[member.id]}"
            )
            break

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await handle_welcome(member)

# ---------------- BASIC COMMANDS ---------------- #

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention} 👋")

# ---------------- RUN BOT ---------------- #

bot.run(TOKEN)
