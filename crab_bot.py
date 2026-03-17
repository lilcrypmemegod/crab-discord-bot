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

# Replace these with your crab-with-knife gifs
crab_gifs = [
    "https://i.imgur.com/3ZQ3Z9E.gif",
    "https://i.imgur.com/B3h9M4Q.gif",
    "https://i.imgur.com/kd7U6sF.gif"
]


class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description="🦀 **SOMEONE PRESSED THE CRAB BUTTON** 🔪",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.send_message(embed=embed)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.command(name="crab")
async def crab(ctx):

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

    embed = discord.Embed(
        description=f"**MC - {mc_text}**\nDO NOT PRESS THE CRAB BUTTON.",
        color=0xff0000
    )

    await ctx.send(embed=embed, view=CrabButton())


bot.run(TOKEN)
