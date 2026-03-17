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
"https://tenor.com/view/licking-knife-crabby-crab-pikaole-threatening-menacing-gif-23124736",
"https://tenor.com/view/fighting-crab-crab-with-a-knife-hes-got-a-knife-dont-touch-me-bro-get-off-gif-18793247",
"https://tenor.com/view/threat-crabby-stabby-knife-stab-angry-gif-8684191936841762266",
"https://tenor.com/view/caranguejo-pandlr-man-crab-knife-pandlrg-faca-caranguejo-gif-13381866007168454019",
"https://tenor.com/view/crab-knife-fight-gif-7305809"
]


class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🚨🦀 **{interaction.user.name} pressed the crab button** 🦀🚨"
        )

        await interaction.followup.send(gif)

        # 1 / 777 blessing
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
        description="**DO NOT PRESS THE CRAB BUTTON**",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=CrabButton())


@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, minutes: int):

    channel = ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    gif = random.choice(crab_gifs)

    await ctx.send(f"🔒 Chat locked for {minutes} minutes 🦀")
    await ctx.send(gif)

    await asyncio.sleep(minutes * 60)

    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    await ctx.send("🔓 Chat unlocked 🦀")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):

    channel = ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    await ctx.send("🔓 Chat manually unlocked 🦀")


bot.run(TOKEN)
