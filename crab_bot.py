@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx, minutes: int, raid_link: str = None):

    global lock_active
    lock_active = True

    await ctx.message.delete()

    channel = ctx.channel
    guild = ctx.guild

    for role in guild.roles:
        if role.permissions.administrator:
            continue

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role, overwrite=overwrite)

    message = "🚨🦀 CRAB RAID LOCKDOWN 🦀🚨\n🔒 Chat locked\n"

    if raid_link:
        message += f"\nRAID HERE:\n{raid_link}\n"

    countdown_msg = await ctx.send(message + f"\nUnlocking in: {minutes} minutes")

    gif = random.choice(crab_gifs)
    await ctx.send(gif)

    remaining = minutes

    while remaining > 0 and lock_active:

        await asyncio.sleep(60)
        remaining -= 1

        if remaining > 0:
            await countdown_msg.edit(
                content=message + f"\nUnlocking in: {remaining} minutes"
            )

    if lock_active:

        for role in guild.roles:
            if role.permissions.administrator:
                continue

            overwrite = channel.overwrites_for(role)
            overwrite.send_messages = None
            await channel.set_permissions(role, overwrite=overwrite)

    lock_active = False
