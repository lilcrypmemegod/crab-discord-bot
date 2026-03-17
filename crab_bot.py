import discord
from discord.ext import commands
import os
import requests
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

PAIR_API = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

crab_gifs = [
    "https://media.giphy.com/media/Y4nmq4GOnLf4XIgALX/giphy.gif",
    "https://media.giphy.com/media/kGdP6qyP3xTS2efTW0/giphy.gif",
    "https://media.giphy.com/media/3o7TKMt1VVNkHV2PaE/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"
]

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command(name="crab")
async def crab(ctx):
    try:
        r = requests.get(PAIR_API)
        data = r.json()

        pair = data["pair"]
        mc = pair.get("marketCap") or pair.get("fdv")

        if mc >= 1_000_000:
            mc_text = f"${round(mc/1_000_000,2)}M"
        elif mc >= 1_000:
            mc_text = f"${round(mc/1_000,2)}K"
        else:
            mc_text = f"${mc}"

        gif = random.choice(crab_gifs)

        await ctx.send(f"🦀🔪 **CRAB WITH KNIFE**\nMC - {mc_text}\n{gif}")

    except Exception as e:
        print(e)
        await ctx.send("MC unavailable 🦀")

bot.run(TOKEN)
