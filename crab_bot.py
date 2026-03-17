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
"https://media.tenor.com/8gZ5vH1K6VMAAAAd/licking-knife-crabby.gif",
"https://media.tenor.com/bx5b3hR9Y2EAAAAd/crab-with-a-knife.gif",
"https://media.tenor.com/Fp7E9n4s2FMAAAAd/crab-stabby.gif",
"https://media.tenor.com/fxL2X4S6zM0AAAAd/man-crab-knife.gif",
"https://media.tenor.com/7M4F2mP0k6YAAAAd/crab-knife-fight.gif"
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

        embed = discord.Embed()
        embed.set_image(url=gif)

        await interaction.followup.send(embed=embed)

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

    embed = discord.Embed()
    embed.set_image(url=gif)

    await ctx.send(embed=embed)

@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description=f"MC - {MC}\n\n**DO NOT PRESS THE CRAB BUTTON**",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())

bot.run(TOKEN)
