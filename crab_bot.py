import discord
from discord.ext import commands
import requests
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

PAIR_URL = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

crab_gifs = [
"https://media.tenor.com/Au4dFOh5s5kAAAAC/licking-knife-crabby-crab.gif",
"https://media.tenor.com/VXH0m2CqzLQAAAAC/crab-with-a-knife.gif",
"https://media.tenor.com/FqJq3hM6nC8AAAAC/stabby-crab.gif",
"https://media.tenor.com/704hC405kqAAAAAC/crab-knife-pandlr.gif",
"https://media.tenor.com/6sHqS4b3ZPAAAAAC/crab-knife-fight.gif"
]

def get_mc():

    try:
        data = requests.get(PAIR_URL).json()
        mc = float(data["pair"]["fdv"])

        if mc >= 1_000_000:
            return f"${mc/1_000_000:.2f}M"
        if mc >= 1_000:
            return f"${mc/1_000:.2f}K"

        return f"${mc:.0f}"

    except:
        return "Unknown"

async def update_mc_nickname():

    await bot.wait_until_ready()

    while not bot.is_closed():

        mc = get_mc()

        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=f"MC - {mc}")
            except:
                pass

        await asyncio.sleep(60)

class CrabButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = interaction.user
        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"🚨🦀 **{user.name} pressed the crab button** 🦀🚨\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.edit_message(embed=embed, view=None)

@bot.event
async def on_ready():

    print(f"Crab bot online as {bot.user}")

    bot.loop.create_task(update_mc_nickname())

@bot.command()
async def crab(ctx):

    mc = get_mc()
    gif = random.choice(crab_gifs)

    embed = discord.Embed(
        description=f"MC - {mc}",
        color=0xff0000
    )

    embed.set_image(url=gif)

    await ctx.send(embed=embed)

    if random.randint(1,777) == 1:

        role = discord.utils.get(ctx.guild.roles, name="crab blessing")

        if role:
            await ctx.author.add_roles(role)

            await ctx.send(
                f"🦀 congratulations {ctx.author.mention} you have received the crab blessing the crab gods have blessed you 🦀"
            )

@bot.command()
async def CRAB(ctx):

    mc = get_mc()

    embed = discord.Embed(
        description=f"MC - {mc}\nDO NOT PRESS THE CRAB BUTTON",
        color=0xff0000
    )

    await ctx.send(embed=embed, view=CrabButton())

bot.run(TOKEN)
