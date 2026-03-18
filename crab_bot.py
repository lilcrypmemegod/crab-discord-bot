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

lock_active = False
RAID_ROLE = "Raid Commander"

# ✅ YOUR TOKEN PAIR (CRONOS)
DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"

crab_gifs = [
"https://media.tenor.com/4s8Kk7Y7k8gAAAAd/crab-dance.gif",
"https://media.tenor.com/6Z3YvE8PpJQAAAAd/crab-knife.gif",
"https://media.tenor.com/8d9b48c7a07f9dcbfcba1cc403a53d58/tenor.gif"
]

# ------------------------
# DEX DATA (FINAL FIX - FDV)
# ------------------------
def get_dex_data():
    try:
        data = requests.get(DEX_URL).json()
        pair = data["pairs"][0]

        mc_raw = pair.get("fdv")  # ✅ THIS FIXES IT

        if mc_raw is None:
            return {"mc": "N/A"}

        mc = float(mc_raw)

        def format_num(n):
            if n >= 1_000_000:
                return f"${n/1_000_000:.2f}M"
            elif n >= 1_000:
                return f"${(int(n/100)/10):.1f}K"
            return f"${int(n)}"

        return {"mc": format_num(mc)}

    except Exception as e:
        print("DEX ERROR:", e)
        return {"mc": "N/A"}


# ------------------------
# 🔥 UPDATE STATUS (GREEN TEXT)
# ------------------------
async def update_mc_status():
    await bot.wait_until_ready()

    while True:
        dex = get_dex_data()
        mc = dex["mc"]

        try:
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"MC - {mc}"
                )
            )
        except:
            pass

        await asyncio.sleep(60)


# ------------------------
# 🔥 UPDATE NICKNAME (REAL FIX)
# ------------------------
async def update_bot_nickname():
    await bot.wait_until_ready()

    while True:
        dex = get_dex_data()
        mc = dex["mc"]

        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=f"MC - {mc}")
            except:
                pass

        await asyncio.sleep(60)


# ------------------------
# BUTTON
# ------------------------
class CrabButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🦀 {interaction.user.mention} pressed the crab button 🦀"
        )

        await interaction.followup.send(gif)

        if random.randint(1,777) == 1:
            await interaction.followup.send(
                f"✨🦀 {interaction.user.mention} received the crab blessing 🦀✨"
            )


# ------------------------
# READY
# ------------------------
@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")

    bot.loop.create_task(update_mc_status())
    bot.loop.create_task(update_bot_nickname())


# ------------------------
# !crab
# ------------------------
@bot.command()
async def crab(ctx):
    await ctx.message.delete()

    gif = random.choice(crab_gifs)
    dex = get_dex_data()

    await ctx.send(f"{gif}\n💰 MC: {dex['mc']}")

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
# LOCK (RAID COMMANDER ONLY)
# ------------------------
@bot.command()
async def lock(ctx, minutes: int, raid_link: str = None):

    global lock_active

    if RAID_ROLE not in [role.name for role in ctx.author.roles]:
        return

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    lock_active = True

    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role, overwrite=overwrite)

    msg = f"🚨🦀 RAID ALERT 🦀🚨\n@everyone\n🔒 Chat locked\n"

    if raid_link:
        msg += f"\n⚔️ RAID HERE ⚔️\n{raid_link}\n"

    countdown_msg = await ctx.send(msg + f"\n⏳ Unlocking in: {minutes} minutes")

    await ctx.send(random.choice(crab_gifs))

    remaining = minutes

    while remaining > 0 and lock_active:
        await asyncio.sleep(60)
        remaining -= 1

        if remaining > 0:
            await countdown_msg.edit(
                content=msg + f"\n⏳ Unlocking in: {remaining} minutes"
            )

    # unlock
    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = None
        await channel.set_permissions(role, overwrite=overwrite)

    lock_active = False

    await ctx.send("🔓 Chat unlocked 🦀")


# ------------------------
# EMERGENCY UNLOCK
# ------------------------
@bot.command()
async def unlock(ctx):

    global lock_active

    if RAID_ROLE not in [role.name for role in ctx.author.roles]:
        return

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    for role in guild.roles:
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = None
        await channel.set_permissions(role, overwrite=overwrite)

    lock_active = False

    await ctx.send("🔓 Emergency unlock 🦀")


bot.run(TOKEN)
