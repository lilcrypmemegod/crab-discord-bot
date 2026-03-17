import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

lock_active = False

crab_gifs = [
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]


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
                f"🦀 congratulations {interaction.user.mention} you have received the crab blessing 🦀"
            )


@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")


@bot.command()
async def crab(ctx):

    await ctx.message.delete()

    gif = random.choice(crab_gifs)
    await ctx.send(gif)


@bot.command(name="CRAB")
async def crab_button(ctx):

    await ctx.message.delete()

    embed = discord.Embed(
        description="🚨 DO NOT PRESS THE CRAB BUTTON 🚨",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())


@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx, minutes: int, raid_link: str = None):

    global lock_active
    lock_active = True

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    # lock every role except admins
    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role, overwrite=overwrite)

    message_text = "🚨🦀 CRAB RAID LOCKDOWN 🦀🚨\n🔒 Chat locked\n"

    if raid_link:
        message_text += f"\nRAID HERE:\n{raid_link}\n"

    countdown_msg = await ctx.send(message_text + f"\nUnlocking in: {minutes} minutes")

    gif = random.choice(crab_gifs)
    await ctx.send(gif)

    remaining = minutes

    while remaining > 0 and lock_active:

        await asyncio.sleep(60)
        remaining -= 1

        if remaining > 0:
            new_text = message_text + f"\nUnlocking in: {remaining} minutes"
            await countdown_msg.edit(content=new_text)

    # unlock silently
    if lock_active:
        for role in guild.roles:
            if role.permissions.administrator:
                continue

            overwrite = channel.overwrites_for(role)
            overwrite.send_messages = None
            await channel.set_permissions(role, overwrite=overwrite)

    lock_active = False


@bot.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):

    global lock_active
    lock_active = False

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = None
        await channel.set_permissions(role, overwrite=overwrite)


bot.run(TOKEN)
