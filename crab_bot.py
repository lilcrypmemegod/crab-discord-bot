import discord
import requests
import os
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

PAIR_API = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

crab_gifs = [
"https://media.tenor.com/3QkS2J8YB5AAAAAC/crabby-crab-pikaole.gif",
"https://media.tenor.com/7K6sR2u9N0AAAAAC/crab-with-a-knife.gif",
"https://media.tenor.com/hWc3J8JxCj0AAAAC/threat-crabby-stabby.gif",
"https://media.tenor.com/lXkZJp2R0KcAAAAC/caraguejo-pandlr.gif",
"https://media.tenor.com/JV5R4J2NQ2kAAAAC/crab-knife-fight.gif"
]


def get_mc():

    try:
        r = requests.get(PAIR_API, timeout=10)
        data = r.json()

        pair = data.get("pair")

        if not pair:
            return "MC unavailable"

        mc = pair.get("marketCap") or pair.get("fdv")

        if not mc:
            return "MC unavailable"

        if mc >= 1_000_000:
            return f"${round(mc/1_000_000,2)}M"

        if mc >= 1_000:
            return f"${round(mc/1_000,2)}K"

        return f"${mc}"

    except:
        return "MC unavailable"


async def crab_blessing(message):

    try:

        roll = random.randint(1,777)

        if roll != 1:
            return

        guild = message.guild
        role_name = "Crab Blessing"

        role = discord.utils.get(guild.roles, name=role_name)

        if role is None:
            role = await guild.create_role(name=role_name)

        await message.author.add_roles(role)

        embed = discord.Embed(
            description=f"🦀 **THE CRAB GODS HAVE SPOKEN**\n\n{message.author.mention} has received the **CRAB BLESSING**",
            color=0xff0000
        )

        embed.set_image(url=random.choice(crab_gifs))

        await message.channel.send(embed=embed)

    except:
        pass


class CrabButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)

    async def press(self, interaction: discord.Interaction, button: discord.ui.Button):

        try:

            mc = get_mc()
            gif = random.choice(crab_gifs)

            embed = discord.Embed(
                description=f"🦀 **{interaction.user.display_name} pressed the crab button 🔪**\n\nMC - {mc}",
                color=0xff0000
            )

            embed.set_image(url=gif)

            await interaction.response.send_message(embed=embed)

        except:
            await interaction.response.send_message("Crab malfunction 🦀", ephemeral=True)


@client.event
async def on_ready():
    print(f"Crab bot running as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    try:

        if message.content == "!crab":

            mc = get_mc()
            gif = random.choice(crab_gifs)

            embed = discord.Embed(
                description=f"MC - {mc}",
                color=0xff0000
            )

            embed.set_image(url=gif)

            await message.channel.send(embed=embed)

            await crab_blessing(message)


        if message.content == "!CRAB":

            mc = get_mc()
            gif = random.choice(crab_gifs)

            embed = discord.Embed(
                description=f"MC - {mc}\nDO NOT PRESS THE CRAB BUTTON",
                color=0xff0000
            )

            embed.set_image(url=gif)

            await message.channel.send(embed=embed, view=CrabButton())

            await crab_blessing(message)

    except:
        pass


client.run(TOKEN)
