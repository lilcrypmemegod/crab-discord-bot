import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# YOUR ORIGINAL KNIFE CRAB GIFS
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


# POST RANDOM CRAB GIF
@bot.command()
async def crab(ctx):

    await ctx.message.delete()

    gif = random.choice(crab_gifs)

    await ctx.send(gif)


# SPAWN CRAB BUTTON
@bot.command(name="CRAB")
async def crab_button(ctx):

    await ctx.message.delete()

    embed = discord.Embed(
        description=f"🚨 DO NOT PRESS THE CRAB BUTTON 🚨\n\nsummoned by {ctx.author.mention}",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())


# RAID LOCK
@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx, minutes: int):

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    overwrite = channel.overwrites_for(guild.default_role)
    overwrite.send_messages = False

    await channel.set_permissions(guild.default_role, overwrite=overwrite)

    await ctx.send("🚨🦀 CRAB RAID LOCKDOWN 🦀🚨\n🔒 Chat locked")

    gif = random.choice(crab_gifs)

    await ctx.send(gif)

    await asyncio.sleep(minutes * 60)

    overwrite.send_messages = None
    await channel.set_permissions(guild.default_role, overwrite=overwrite)


bot.run(TOKEN)
