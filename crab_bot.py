import discord
from discord.ext import commands
import requests
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

PAIR_API = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

crab_gifs = [
"https://media.tenor.com/Au4dFOh5s5kAAAAC/licking-knife-crabby-crab.gif",
"https://media.tenor.com/VXH0m2CqzLQAAAAC/crab-with-a-knife.gif",
"https://media.tenor.com/FqJq3hM6nC8AAAAC/stabby-crab.gif",
"https://media.tenor.com/704hC405kqAAAAAC/crab-knife-pandlr.gif",
"https://media.tenor.com/6sHqS4b3ZPAAAAAC/crab-knife-fight.gif"
]


def get_mc():
    try:
        r = requests.get(PAIR_API, timeout=10)
        data = r.json()

        pair = data["pair"]
        mc = pair.get("marketCap") or pair.get("fdv")

        if mc >= 1_000_000:
            return f"${round(mc/1_000_000,2)}M"

        if mc >= 1_000:
            return f"${round(mc/1_000,2)}K"

        return f"${mc}"

    except:
        return "MC unavailable"


async def crab_blessing(ctx):

    if random.randint(1,777) != 1:
        return

    role_name = "crab blessing"

    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        role = await ctx.guild.create_role(name=role_name)

    await ctx.author.add_roles(role)

    username = ctx.author.display_name

    embed = discord.Embed(
        title="🦀 CRAB BLESSING 🦀",
        description=f"🦀 **Congratulations {username}!**\n\nYou have received the **crab blessing**.\nThe crab gods have blessed you. 🦀",
        color=0xff0000
    )

    embed.set_image(url=random.choice(crab_gifs))

    await ctx.send(embed=embed)


class CrabButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)

    async def crab_press(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = get_mc()
        gif = random.choice(crab_gifs)

        embed = discord.Embed(
            description=f"🦀 **{interaction.user.display_name} pressed the crab button**\n\nMC - {mc}",
            color=0xff0000
        )

        embed.set_image(url=gif)

        await interaction.response.edit_message(embed=embed, view=None)


@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")


@bot.command()
async def crab(ctx):

    mc = get_mc()

    embed = discord.Embed(
        description=f"MC - {mc}",
        color=0xff0000
    )

    embed.set_image(url=random.choice(crab_gifs))

    await ctx.send(embed=embed)

    await crab_blessing(ctx)


@bot.command()
async def CRAB(ctx):

    mc = get_mc()

    embed = discord.Embed(
        description=f"MC - {mc}\n\n**DO NOT PRESS THE CRAB BUTTON**",
        color=0xff0000
    )

    await ctx.send(embed=embed, view=CrabButton())

    await crab_blessing(ctx)


bot.run(TOKEN)
