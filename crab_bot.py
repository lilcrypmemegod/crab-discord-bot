import os
import discord
from discord.ext import commands
import requests

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def crab(ctx):
    try:
        url = "https://api.dexscreener.com/latest/dex/search/?q=crab"
        response = requests.get(url)

        if response.status_code != 200:
            await ctx.send("API error. Try again later.")
            return

        data = response.json()

        if not data or "pairs" not in data or len(data["pairs"]) == 0:
            await ctx.send("Could not find CRAB token data.")
            return

        pair = data["pairs"][0]

        price = pair["priceUsd"]
        liquidity = pair["liquidity"]["usd"]
        volume = pair["volume"]["h24"]

        message = (
            f"🦀 **CRAB Token Info**\n"
            f"Price: ${price}\n"
            f"Liquidity: ${liquidity}\n"
            f"24h Volume: ${volume}"
        )

        await ctx.send(message)

    except Exception as e:
        print(e)
        await ctx.send("Something went wrong fetching CRAB data.")


bot.run(TOKEN)
