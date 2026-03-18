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

# ----------------
# DEX DATA (FIXED MC)
# ----------------

def get_dex_data():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/cronos/0xdf9030e28cde0f4e6f11c65362c5e152093c7414"
        data = requests.get(url).json()["pair"]

        # ✅ FIX: use marketCap instead of fdv
        mc = float(data.get("marketCap", data.get("fdv", 0)))
        liquidity = float(data["liquidity"]["usd"])
        change = float(data["priceChange"]["h24"])

        def format_num(n):
            if n >= 1_000_000:
                return f"${n/1_000_000:.2f}M"
            elif n >= 1_000:
                return f"${n/1_000:.1f}K"
            return f"${n:.0f}"

        return {
            "mc": format_num(mc),
            "liq": format_num(liquidity),
            "change": f"{change:+.2f}%"
        }

    except:
        return {
            "mc": "N/A",
            "liq": "N/A",
            "change": "N/A"
        }


# ----------------
# ROTATING STATUS
# ----------------

async def rotate_status():
    await bot.wait_until_ready()

    while not bot.is_closed():

        data = get_dex_data()

        statuses = [
            f"MC - {data['mc']}",
            f"Liquidity - {data['liq']}",
            f"24H - {data['change']}"
        ]

        for status in statuses:
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=status
                )
            )
            await asyncio.sleep(15)


# ----------------
# CRAB GIFS
# ----------------

crab_gifs = [
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]


# ----------------
# ROLE CHECK
# ----------------

def is_raid_commander():
    async def predicate(ctx):
        return any(role.name == RAID_ROLE for role in ctx.author.roles)
    return commands.check(predicate)


# ----------------
# BUTTON
# ----------------

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
                f"✨🦀 CRAB BLESSING 🦀✨\n{interaction.user.mention} has been chosen"
            )


# ----------------
# READY
# ----------------

@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")
    bot.loop.create_task(rotate_status())


# ----------------
# PUBLIC COMMANDS
# ----------------

@bot.command()
async def crab(ctx):

    gif = random.choice(crab_gifs)
    await ctx.send(gif)

    if random.randint(1,777) == 1:
        await ctx.send(
            f"✨🦀 CRAB BLESSING 🦀✨\n{ctx.author.mention} has been chosen"
        )


@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description="🚨 DO NOT PRESS THE CRAB BUTTON 🚨",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())


# ----------------
# RAID COMMANDS
# ----------------

@bot.command()
@is_raid_commander()
async def lock(ctx, minutes: int, raid_link: str):

    global lock_active
    lock_active = True

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    gif = random.choice(crab_gifs)

    message = await ctx.send(
        f"🚨🦀 **RAID ALERT** 🦀🚨\n"
        f"@everyone\n\n"
        f"⚔ RAID HERE ⚔\n{raid_link}\n\n"
        f"🔒 Chat locked\n"
        f"⏳ Unlocking in: {minutes} minutes"
    )

    await ctx.send(gif)

    overwrite = channel.overwrites_for(guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(guild.default_role, overwrite=overwrite)

    remaining = minutes

    while remaining > 0 and lock_active:
        await asyncio.sleep(60)
        remaining -= 1

        if remaining > 0:
            await message.edit(
                content=
                f"🚨🦀 **RAID ALERT** 🦀🚨\n"
                f"@everyone\n\n"
                f"⚔ RAID HERE ⚔\n{raid_link}\n\n"
                f"🔒 Chat locked\n"
                f"⏳ Unlocking in: {remaining} minutes"
            )

    if lock_active:
        overwrite = channel.overwrites_for(guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(guild.default_role, overwrite=overwrite)

        await ctx.send("🔓 Chat unlocked 🦀")

    lock_active = False


@bot.command()
@is_raid_commander()
async def unlock(ctx):

    global lock_active
    lock_active = False

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    overwrite = channel.overwrites_for(guild.default_role)
    overwrite.send_messages = None
    await channel.set_permissions(guild.default_role, overwrite=overwrite)

    await ctx.send("🔓 Chat unlocked 🦀")


bot.run(TOKEN)
