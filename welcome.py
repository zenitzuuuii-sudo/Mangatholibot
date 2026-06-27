import discord
from welcome_card import create_card

WELCOME_CHANNEL_ID = 0  # Replace with your welcome channel ID


async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    card = await create_card(member)
    await channel.send(
        f"Welcome to **{member.guild.name}**, {member.mention}! 🎉",
        file=discord.File(fp=card, filename="welcome.png")
    )
