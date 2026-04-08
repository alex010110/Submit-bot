import discord
import os
import asyncio

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1490799686687391894  # Your server ID

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    # Fetch all guild commands
    commands = await tree.fetch_guild_commands(guild.id)

    submit_commands = [cmd for cmd in commands if cmd.name == "submit"]
    if not submit_commands:
        print("✅ No /submit commands found. Nothing to delete.")
        await client.close()
        return

    # Delete all /submit commands
    for cmd in submit_commands:
        await tree.delete_guild_command(cmd.id, guild.id)
        print(f"Deleted command: {cmd.name} ({cmd.id})")

    print("✅ All old /submit commands have been removed.")
    await client.close()

async def main():
    await client.start(TOKEN)

asyncio.run(main())