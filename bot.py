import discord
import asyncio
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1490799686687391894

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    # Clear global commands
    tree.clear_commands(guild=None)
    await tree.sync()
    print("Global commands cleared.")

    # Clear guild commands
    guild = discord.Object(id=GUILD_ID)
    tree.clear_commands(guild=guild)
    await tree.sync(guild=guild)
    print("Guild commands cleared.")

    await client.close()

client.run(TOKEN)