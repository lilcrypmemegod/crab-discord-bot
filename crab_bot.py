import discord
import requests
import os
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

PAIR_API = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

crab_gifs = [
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]


def get_mc():
    try:
        r = requests.get(PAIR_API, timeout=10)
        data = r.json()

        pair = data.get("pair")
        mc = pair.get("marketCap") or pair.get("fdv")

        if mc >= 1_000_000:
            return f"${round(mc/1_000_000,2)}M"
        if mc >= 1_000:
            return f"${round(mc/1_000,2)}K"

        return f"${mc}"

    except:
        return "MC unavailable"


class CrabButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)

    async def press(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            title="CRAB BUTTON PRESSED",
            description=f"🦀 **{interaction.user.display_name} pressed the crab button**\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        # remove button
        await interaction.response.edit_message(embed=embed, view=None)


@client.event
async def on_ready():
    print(f"Crab bot running as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "!CRAB":

        mc = get_mc()

        embed = discord.Embed(
            description=f"MC - {mc}\n\n**DO NOT PRESS THE CRAB BUTTON**",
            color=0xff0000
        )

        await message.channel.send(embed=embed, view=CrabButton())


client.run(TOKEN)
