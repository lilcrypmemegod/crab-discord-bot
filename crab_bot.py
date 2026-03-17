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

    await ctx.send(
        f"🦀 **Congratulations {username}!**\n"
        f"You have received the **crab blessing**.\n"
        f"The crab gods have blessed you. 🦀"
    )

    await ctx.send(random.choice(crab_gifs))


class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)

    async def crab_press(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = get_mc()
        gif = random.choice(crab_gifs)

        await interaction.response.edit_message(
            content=f"🦀 **{interaction.user.display_name} pressed the crab button**\n\nMC - {mc}",
            view=None
        )

        await interaction.channel.send(gif)


@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")


@bot.command()
async def crab(ctx):

    mc = get_mc()

    await ctx.send(f"MC - {mc}")

    await ctx.send(random.choice(crab_gifs))

    await crab_blessing(ctx)


@bot.command()
async def CRAB(ctx):

    mc = get_mc()

    await ctx.send(
        f"MC - {mc}\n\n**DO NOT PRESS THE CRAB BUTTON**",
        view=CrabButton()
    )

    await crab_blessing(ctx)


bot.run(TOKEN)
