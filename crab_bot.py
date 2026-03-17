import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# knife crab gifs (embed properly)
crab_gifs = [
"https://media.tenor.com/8d9b48c7a07f9dcbfcba1cc403a53d58/tenor.gif",
"https://media.tenor.com/1f21d71f7d23d5d7d64f3f7e5f6e4f3c/tenor.gif",
"https://media.tenor.com/2g7uGZ6q9x0AAAAd/crab-battle.gif",
"https://media.tenor.com/4s8Kk7Y7k8gAAAAd/crab-dance.gif",
"https://media.tenor.com/6Z3YvE8PpJQAAAAd/crab-knife.gif"
]


class CrabButton(discord.ui.View):

    @discord.ui.button(label="CRAB", style=discord.ButtonStyle.danger)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):

        gif = random.choice(crab_gifs)

        button.disabled = True
        button.label = "CRABBED"

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"🦀 {interaction.user.name} pressed the crab button 🦀"
        )

        embed = discord.Embed(color=discord.Color.red())
        embed.set_image(url=gif)

        await interaction.followup.send(embed=embed)

        if random.randint(1,777) == 1:
            await interaction.followup.send(
                f"🦀 congratulations {interaction.user.mention} you have received the crab blessing 🦀"
            )


@bot.event
async def on_ready():
    print(f"Crab bot online as {bot.user}")


# crab gif command
@bot.command()
async def crab(ctx):

    await ctx.message.delete()

    gif = random.choice(crab_gifs)

    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=gif)

    await ctx.send(embed=embed)


# crab button command
@bot.command(name="CRAB")
async def crab_button(ctx):

    await ctx.message.delete()

    embed = discord.Embed(
        description="🚨 DO NOT PRESS THE CRAB BUTTON 🚨",
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

    gif = random.choice(crab_gifs)

    await ctx.send("🚨🦀 CRAB RAID LOCKDOWN 🦀🚨\n🔒 Chat locked")

    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=gif)

    await ctx.send(embed=embed)

    await asyncio.sleep(minutes * 60)

    overwrite.send_messages = True
    await channel.set_permissions(guild.default_role, overwrite=overwrite)

    await ctx.send("🔓 Chat unlocked 🦀")


# UNLOCK COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    overwrite = channel.overwrites_for(guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(guild.default_role, overwrite=overwrite)

    await ctx.send("🔓 Chat unlocked 🦀")


bot.run(TOKEN)
