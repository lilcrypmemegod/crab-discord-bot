import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

crab_gifs = [
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]

async def get_mc(channel):
    async for msg in channel.history(limit=20):
        if "MC -" in msg.content:
            return msg.content
    return "MC - Unknown"

class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        mc = await get_mc(interaction.channel)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🚨🦀 **{interaction.user.name} pressed the crab button** 🦀🚨\n{mc}"
        )

        gif = random.choice(crab_gifs)

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

    mc = await get_mc(ctx.channel)

    gif = random.choice(crab_gifs)

    await ctx.send(mc)
    await ctx.send(gif)

@bot.command(name="CRAB")
async def crab_button(ctx):

    mc = await get_mc(ctx.channel)

    embed = discord.Embed(
        description=f"{mc}\n\n**DO NOT PRESS THE CRAB BUTTON**",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())

bot.run(TOKEN)
