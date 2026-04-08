import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1490799686687391894
ALLOWED_CHANNEL_ID = 1491100377754370159
ART_SUBMISSIONS_CHANNEL_ID = 1491190135822483487
REQUIRED_ROLE_NAME = "Novice of Shadows [Lvl 5+]"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="submit",
    description="Submit your art to the art submissions channel!",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    file="Upload your artwork file here",
    description="Describe your artwork"
)
async def submit(interaction: discord.Interaction, file: discord.Attachment, description: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command in this channel.",
            ephemeral=True
        )
        return

    role_names = [role.name for role in interaction.user.roles]
    if REQUIRED_ROLE_NAME not in role_names:
        await interaction.response.send_message(
            f"❌ You need the **{REQUIRED_ROLE_NAME}** role to submit art.",
            ephemeral=True
        )
        return

    embed = discord.Embed(title="🎨 New Art Submission!", color=0xE91E8C)
    embed.add_field(name="👤 Artist", value=f"<@{interaction.user.id}> ({interaction.user.name})", inline=False)
    embed.add_field(name="📝 Description", value=description, inline=False)
    embed.set_footer(text="Art Submissions")
    embed.timestamp = interaction.created_at

    art_channel = client.get_channel(ART_SUBMISSIONS_CHANNEL_ID)
    await art_channel.send(embed=embed, file=await file.to_file())

    await interaction.response.send_message(
        "✅ Your submission has been sent to #art-submissions!",
        ephemeral=True
    )

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    
    # Delete old guild commands to prevent duplicates
    for cmd in await tree.fetch_commands(guild=guild):
        await tree.delete_command(cmd.id, guild=guild)
    
    await tree.sync(guild=guild)
    print(f"Bot is online as {client.user} and commands synced")

client.run(TOKEN)