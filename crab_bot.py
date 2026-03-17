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
"https://media.tenor.com/9Y6n4d4V3eUAAAAC/crab-knife.gif",
"https://media.tenor.com/NqKNh7Q5hL8AAAAC/crab-knife-crab.gif",
"https://media.tenor.com/YZ9JX3KX6xYAAAAC/crab-dance-knife.gif"
]


def get_mc():

    r = requests.get(PAIR_API)
    data = r.json()

    pair = data["pair"]
    mc = pair.get("marketCap") or pair.get("fdv")

    if mc >= 1_000_000:
        return f"${round(mc/1_000_000,2)}M"
    elif mc >= 1_000:
        return f"${round(mc/1_000,2)}K"
    else:
        return f"${mc}"


class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)
        mc = get_mc()

        embed = discord.Embed(
            description=f"🦀 **SOMEONE PRESSED THE CRAB BUTTON** 🔪\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.send_message(embed=embed)


@bot.command(name="crab")
async def crab(ctx):

    mc = get_mc()
    gif = random.choice(crab_gifs)

    user_text = ctx.message.content

    # LOWERCASE COMMAND
    if user_text.startswith("!crab") and not user_text.startswith("!CRAB"):

        embed = discord.Embed(
            description=f"MC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await ctx.send(embed=embed)


    # UPPERCASE COMMAND
    if user_text.startswith("!CRAB"):

        embed = discord.Embed(
            description=f"MC - {mc}\nDO NOT PRESS THE CRAB BUTTON.",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await ctx.send(embed=embed, view=CrabButton())


bot.run(TOKEN)
