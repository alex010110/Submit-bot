import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1490799686687391894
ALLOWED_CHANNEL_ID = 1491100377754370159
REQUIRED_ROLE = "Novice of Shadows [Lvl 5+]"
ART_SUBMISSIONS_CHANNEL_ID = 1491190135822483487

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Hide the command in other channels
@tree.before_invoke
async def check_channel(interaction: discord.Interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        raise app_commands.CheckFailure("This command cannot be used in this channel.")
    if REQUIRED_ROLE not in [role.name for role in interaction.user.roles]:
        raise app_commands.CheckFailure("You do not have the required role.")

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            str(error),
            ephemeral=True
        )

@tree.command(
    name="submit",
    description="Submit your art to the art submissions channel!"
)
@app_commands.describe(
    file="Upload your artwork file here",
    description="Describe your artwork"
)
async def submit(interaction: discord.Interaction, file: discord.Attachment, description: str):
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
            description=f"✅ Your submission has been sent to <#{ART_SUBMISSIONS_CHANNEL_ID}>!",
            color=0x57F287
        ),
        ephemeral=True
    )

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)
    print(f"Bot is online as {client.user} and commands synced in guild {GUILD_ID}!")

client.run(TOKEN)