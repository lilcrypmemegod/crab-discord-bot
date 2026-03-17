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
"https://media.tenor.com/Z6gmDPeM6dgAAAAC/crab-dance.gif",
"https://media.tenor.com/W5gq7HnYx6QAAAAC/crab-rave.gif",
"https://media.tenor.com/f8dZ8iKz9hAAAAAC/crab-dance-party.gif"
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
    async def press(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"🦀 SOMEONE PRESSED THE CRAB BUTTON 🔪\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    print("Crab bot ready")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # !crab command
    if message.content == "!crab":

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"MC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await message.channel.send(embed=embed)

    # !CRAB command
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
