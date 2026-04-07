import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")
ART_SUBMISSIONS_CHANNEL_ID = 1491190135822483487
ALLOWED_COMMAND_CHANNEL_ID = 1491100377754370159
REQUIRED_ROLE_NAME = "Novice of Shadows [Lvl 5+]"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Replace with your server ID
GUILD_ID = 123456789012345678  # put your server ID here

@tree.command(
    name="submit",
    description="Submit your art to the art submissions channel!",
    guild=discord.Object(id=GUILD_ID)  # limit command to your server
)
@app_commands.describe(
    file="Upload your artwork file here",
    description="Describe your artwork"
)
async def submit(interaction: discord.Interaction, file: discord.Attachment, description: str):
    
    # Check if user has required role
    role_names = [role.name for role in interaction.user.roles]
    if REQUIRED_ROLE_NAME not in role_names:
        await interaction.response.send_message(
            f"❌ You need the '{REQUIRED_ROLE_NAME}' role to use this command!",
            ephemeral=True
        )
        return

    # Create the embed for submission
    embed = discord.Embed(title="🎨 New Art Submission!", color=0xE91E8C)
    embed.add_field(name="👤 Artist", value=f"<@{interaction.user.id}> ({interaction.user.name})", inline=False)
    embed.add_field(name="📝 Description", value=description, inline=False)
    embed.set_footer(text="Art Submissions")
    embed.timestamp = interaction.created_at

    channel = client.get_channel(ART_SUBMISSIONS_CHANNEL_ID)

    await channel.send(
        embed=embed,
        file=await file.to_file()
    )

    await interaction.response.send_message(
        embed=discord.Embed(
            description="✅ Your submission has been sent to #art-submissions!",
            color=0x57F287
        ),
        ephemeral=True
    )

@client.event
async def on_ready():
    # Sync commands only to this guild
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Bot is online as {client.user}")

client.run(TOKEN)