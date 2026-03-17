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
"https://media.tenor.com/28m_uG2B0K4AAAAd/crab-with-knife.gif",
"https://media.tenor.com/ksGxk8KZc4kAAAAd/crab-fight.gif",
"https://media.tenor.com/2g7uGZ6q9x0AAAAd/crab-battle.gif",
"https://media.tenor.com/X3G8W2WfK1kAAAAd/crab-knife-fight.gif",
"https://media.tenor.com/bn6wVnH3v6gAAAAd/crab-knife.gif"
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
                f"🦀✨ CRAB GOD EVENT ✨🦀\n\ncongratulations {interaction.user.mention} you have received the crab blessing the crab gods have blessed you 🦀"
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
