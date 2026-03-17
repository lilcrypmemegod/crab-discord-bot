import discord
from discord.ext import commands
import os
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

crab_memes = [
    "🦀 CRAB WITH KNIFE",
    "🦀 SNIP SNIP",
    "🦀 CRAB MODE ACTIVATED",
]

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command()
async def crab(ctx):
    await ctx.send(random.choice(crab_memes))

@bot.command()
async def hello(ctx):
    await ctx.send("hello 🦀")

@bot.command()
async def price(ctx):
    await ctx.send("CRAB price coming soon 🦀")

bot.run(TOKEN)
