import discord
from discord.ext import commands
import requests
import os

TOKEN = os.getenv("TOKEN")
TOKEN_ADDRESS = "0xC84398E9BBBC028BA81621DC45194049D173Ef"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"CRAB BOT ONLINE: {bot.user}")

@bot.command()
async def crab(ctx):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}"
    data = requests.get(url).json()

    pair = data["pairs"][0]

    price = pair["priceUsd"]
    mcap = pair["fdv"]

    embed = discord.Embed(
        title="🦀 CRAB TOKEN",
        color=0xff0000
    )

    embed.add_field(name="Price", value=f"${price}", inline=False)
    embed.add_field(name="Market Cap", value=f"${mcap}", inline=False)

    await ctx.send(embed=embed)

bot.run(TOKEN)
