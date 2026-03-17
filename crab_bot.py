import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MC = "$35.56K"

# Direct Tenor CDN GIF links (these embed correctly)
crab_gifs = [
"https://media.tenor.com/28m_uG2B0K4AAAAd/crab-with-knife.gif",
"https://media.tenor.com/X3G8W2WfK1kAAAAd/crab-with-knife-fight.gif",
"https://media.tenor.com/ksGxk8KZc4kAAAAd/crab-fight.gif",
"https://media.tenor.com/2g7uGZ6q9x0AAAAd/crab-battle.gif",
"https://media.tenor.com/bn6wVnH3v6gAAAAd/crab-knife.gif"
]

class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        press_embed = discord.Embed(
            description=f"🚨🦀 {interaction.user.name} pressed the crab button 🦀🚨\n\nMC - {MC}",
            color=discord.Color.red()
        )

        gif_embed = discord.Embed()
        gif_embed.set_image(url=gif)

        await interaction.followup.send(embed=press_embed)
        await interaction.followup.send(embed=gif_embed)

        await interaction.followup.send(
            f"🦀 congratulations {interaction.user.mention} you have received the crab blessing the crab gods have blessed you 🦀"
        )

@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")

@bot.command()
async def crab(ctx):

    gif = random.choice(crab_gifs)

    mc_embed = discord.Embed(
        description=f"MC - {MC}",
        color=discord.Color.red()
    )

    gif_embed = discord.Embed()
    gif_embed.set_image(url=gif)

    await ctx.send(embed=mc_embed)
    await ctx.send(embed=gif_embed)

@bot.command(name="CRAB")
async def crab_button(ctx):

    embed = discord.Embed(
        description=f"MC - {MC}\n\nDO NOT PRESS THE CRAB BUTTON",
        color=discord.Color.dark_red()
    )

    await ctx.send(embed=embed, view=CrabButton())

bot.run(TOKEN)
