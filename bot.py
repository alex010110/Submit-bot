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

GUILD = discord.Object(id=GUILD_ID)  # Define once, reuse everywhere

@tree.command(
    name="submit",
    description="Submit your art to the art submissions channel!",
    guild=GUILD  # ← THIS was missing
)
@app_commands.describe(
    file="Upload your artwork file here",
    description="Describe your artwork"
)
async def submit(interaction: discord.Interaction, file: discord.Attachment, description: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>.",
            ephemeral=True
        )
        return

    role_names = [role.name for role in interaction.user.roles]
    if REQUIRED_ROLE_NAME not in role_names:
        await interaction.response.send_message(
            f"❌ You need the **{REQUIRED_ROLE_NAME}** role to submit.",
            ephemeral=True
        )
        return

    channel = client.get_channel(ART_SUBMISSIONS_CHANNEL_ID)
    embed = discord.Embed(title="🎨 New Art Submission!", color=0xE91E8C)
    embed.add_field(name="👤 Artist", value=f"{interaction.user.mention}", inline=False)
    embed.add_field(name="📝 Description", value=description, inline=False)
    embed.set_footer(text="Art Submissions")
    embed.timestamp = interaction.created_at

    await channel.send(embed=embed, file=await file.to_file())
    await interaction.response.send_message(
        embed=discord.Embed(
            description=f"✅ Your submission has been sent to <#{ART_SUBMISSIONS_CHANNEL_ID}>!",
            color=0x57F287
        ),
        ephemeral=True
    )
    print(f"Submission from {interaction.user} forwarded to art channel.")

@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f"Bot is online as {client.user} and commands synced!")

client.run(TOKEN)