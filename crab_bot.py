import discord
import requests
import os
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

PAIR_API = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

# Reliable crab gifs
crab_gifs = [
"https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
"https://media.giphy.com/media/3o7TKsQ8UQ6QWq9G9y/giphy.gif",
"https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
"https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif"
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

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab_press(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = get_mc()
        gif = random.choice(crab_gifs)
        user = interaction.user.display_name

        embed = discord.Embed(
            description=f"🦀 **{user} pressed the crab button 🔪**\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    print(f"Crab bot ready as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return


    # !crab
    if message.content == "!crab":

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"MC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await message.channel.send(embed=embed)


    # !CRAB
    if message.content == "!CRAB":

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"MC - {mc}\nDO NOT PRESS THE CRAB BUTTON",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await message.channel.send(embed=embed, view=CrabButton())


client.run(TOKEN)
