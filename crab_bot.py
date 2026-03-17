import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MC = "$35.56K"

crab_gifs = [
"https://media.tenor.com/images/6c9d1b2d3c8dbe5285bdcf0584d29c0e/tenor.gif",
"https://media.tenor.com/images/8d9b48c7a07f9dcbfcba1cc403a53d58/tenor.gif",
"https://media.tenor.com/images/1f21d71f7d23d5d7d64f3f7e5f6e4f3c/tenor.gif",
"https://media.tenor.com/images/9b3f9e7b1d0c3a7c2b6c0bba2d3b77c0/tenor.gif",
"https://media.tenor.com/images/cfb94f7f8e5f19c6e54c90c6e2c5e9fb/tenor.gif"
]

class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🚨🦀 **{interaction.user.name} pressed the crab button** 🦀🚨\nMC - {MC}"
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

    await ctx.send(f"MC - {MC}")
    await ctx.send(gif)

@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description=f"MC - {MC}\n\n**DO NOT PRESS THE CRAB BUTTON**",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())

bot.run(TOKEN)
