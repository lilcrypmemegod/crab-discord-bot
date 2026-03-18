import discord
from discord.ext import commands
import random
import asyncio
import os
import requests
import aiohttp
import io
import re

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

RAID_ROLE = "Raid Commander"

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

# ✅ YOUR TENOR LINKS
crab_gifs = [
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]

# ------------------------
# GET MC
# ------------------------
def get_mc():
    try:
        data = requests.get(DEX_URL).json()
        pair = data["pairs"][0]
        mc = float(pair.get("fdv", 0))

        if mc >= 1_000_000:
            return f"${mc/1_000_000:.2f}M"
        elif mc >= 1_000:
            return f"${(int(mc/100)/10):.1f}K"
        return f"${int(mc)}"
    except:
        return "N/A"

# ------------------------
# UPDATE BOT NAME
# ------------------------
async def update_mc():
    await bot.wait_until_ready()

    while True:
        mc = get_mc()

        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=f"MC - {mc}")
            except:
                pass

        await asyncio.sleep(60)

# ------------------------
# 🔥 EXTRACT REAL GIF
# ------------------------
async def extract_gif(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()

                match = re.search(r'https://media\.tenor\.com/[^"]+\.gif', html)
                if match:
                    return match.group(0)
    except:
        return None

# ------------------------
# SEND GIF
# ------------------------
async def send_gif(channel):
    url = random.choice(crab_gifs)

    real_gif = await extract_gif(url)

    if real_gif:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(real_gif) as resp:
                    data = await resp.read()
                    file = discord.File(io.BytesIO(data), filename="crab.gif")
                    await channel.send(file=file)
                    return
        except:
            pass

    await channel.send("❌ GIF failed")

# ------------------------
# BUTTON
# ------------------------
class CrabButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🦀 {interaction.user.mention} pressed the crab button 🦀"
        )

        await send_gif(interaction.channel)

        if random.randint(1,777) == 1:
            await interaction.followup.send(
                f"✨🦀 {interaction.user.mention} received the crab blessing 🦀✨"
            )

# ------------------------
# READY
# ------------------------
@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    bot.loop.create_task(update_mc())

# ------------------------
# !crab
# ------------------------
@bot.command()
async def crab(ctx):
    await send_gif(ctx.channel)

    if random.randint(1,777) == 1:
        await ctx.send(f"✨🦀 {ctx.author.mention} received the crab blessing 🦀✨")

# ------------------------
# !CRAB
# ------------------------
@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description="🚨 DO NOT PRESS THE CRAB BUTTON 🚨",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())

# ------------------------
# LOCK
# ------------------------
@bot.command()
async def lock(ctx, minutes: int, raid_link: str = None):

    if RAID_ROLE not in [r.name for r in ctx.author.roles]:
        return

    channel = ctx.channel
    guild = ctx.guild

    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role, overwrite=overwrite)

    msg = f"🚨🦀 RAID ALERT 🦀🚨\n@everyone\n🔒 Chat locked\n"

    if raid_link:
        msg += f"\n⚔️ RAID HERE ⚔️\n{raid_link}\n"

    countdown = await ctx.send(msg + f"\n⏳ {minutes} minutes")

    await send_gif(channel)

    while minutes > 0:
        await asyncio.sleep(60)
        minutes -= 1
        if minutes > 0:
            await countdown.edit(content=msg + f"\n⏳ {minutes} minutes")

    for role in guild.roles:
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = None
        await channel.set_permissions(role, overwrite=overwrite)

    await ctx.send("🔓 Chat unlocked 🦀")

# ------------------------
# UNLOCK
# ------------------------
@bot.command()
async def unlock(ctx):

    if RAID_ROLE not in [r.name for r in ctx.author.roles]:
        return

    for role in ctx.guild.roles:
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(role, overwrite=overwrite)

    await ctx.send("🔓 Emergency unlock 🦀")

bot.run(TOKEN)
