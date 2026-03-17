import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

crab_gifs = [
"https://media.tenor.com/images/8d9b48c7a07f9dcbfcba1cc403a53d58/tenor.gif",
"https://media.tenor.com/images/1f21d71f7d23d5d7d64f3f7e5f6e4f3c/tenor.gif",
"https://media.tenor.com/images/2g7uGZ6q9x0AAAAd/crab-battle.gif",
"https://media.tenor.com/images/4s8Kk7Y7k8gAAAAd/crab-dance.gif"
]

class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🚨🦀 **CRAB RAID ALERT** 🦀🚨\n"
            f"@everyone\n"
            f"**{interaction.user.name} HAS SUMMONED THE CRABS**"
        )

        await interaction.followup.send(gif)

        if random.randint(1,777) == 1:
            await interaction.followup.send(
                f"🦀 congratulations {interaction.user.mention} you have received the crab blessing the crab gods have blessed you 🦀"
            )

@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")

@bot.command()
async def crab(ctx):

    gif = random.choice(crab_gifs)
    await ctx.send(gif)

@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description="🚨 **DO NOT PRESS THE CRAB BUTTON** 🚨",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())

@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx, minutes: int):

    channel = ctx.channel

    await channel.edit(slowmode_delay=21600)

    gif = random.choice(crab_gifs)

    await ctx.send(
        f"🚨🦀 **CRAB RAID LOCKDOWN** 🦀🚨\n"
        f"Chat locked by **{ctx.author.name}** for {minutes} minutes"
    )

    await ctx.send(gif)

    await asyncio.sleep(minutes * 60)

    await channel.edit(slowmode_delay=0)

    await ctx.send("🔓 Raid lockdown ended. Chat reopened 🦀")

@bot.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):

    channel = ctx.channel

    await channel.edit(slowmode_delay=0)

    await ctx.send("🔓 Admin unlocked the chat 🦀")

bot.run(TOKEN)
