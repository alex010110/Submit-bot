import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")
ART_SUBMISSIONS_CHANNEL_ID = 1491190135822483487

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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

    # Send the embed with the file attached
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
    await tree.sync()
    print(f"Bot is online as {client.user}")

client.run(TOKEN)