import discord
from discord.ext import commands
import random
import asyncio
import os
import requests

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

RAID_ROLE = "Raid Commander"
lock_active = False

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

# ✅ YOUR TENOR GIFS (WORK WITH EMBEDS)
crab_gifs = [
"https://media.tenor.com/4s8Kk7Y7k8gAAAAd/crab-dance.gif",
"https://media.tenor.com/6Z3YvE8PpJQAAAAd/crab-knife.gif",
"https://media.tenor.com/8d9b48c7a07f9dcbfcba1cc403a53d58/tenor.gif"
]

# ------------------------
# GET MC (FDV)
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
# 🔥 UPDATE BOT NAME (GREEN)
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

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"MC - {mc}"
            )
        )

        await asyncio.sleep(60)


# ------------------------
# ✅ FORCE GIF EMBED (THIS FIXES EVERYTHING)
# ------------------------
async def send_gif(channel):
    gif = random.choice(crab_gifs)

    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=gif)

    await channel.send(embed=embed)


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

        # ✅ FIXED GIF
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
# !crab (CLEAN)
# ------------------------
@bot.command()
async def crab(ctx):
    await ctx.message.delete()

    await send_gif(ctx.channel)

    if random.randint(1,777) == 1:
        await ctx.send(f"✨🦀 {ctx.author.mention} received the crab blessing 🦀✨")


# ------------------------
# !CRAB BUTTON
# ------------------------
@bot.command(name="CRAB")
async def crab_button(ctx):
    await ctx.message.delete()

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

    await ctx.message.delete()

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

    await ctx.message.delete()

    for role in ctx.guild.roles:
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(role, overwrite=overwrite)

    await ctx.send("🔓 Emergency unlock 🦀")


bot.run(TOKEN)
