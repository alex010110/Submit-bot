import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1490799686687391894
COMMAND_CHANNEL_ID = 1491100377754370159
ART_SUBMISSIONS_CHANNEL_ID = 1491190135822483487
REQUIRED_ROLE_NAME = "Novice of Shadows [Lvl 5+]"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Check role and channel
def can_use_submit():
    async def predicate(interaction: discord.Interaction):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            await interaction.response.send_message(
                f"❌ This command can only be used in <#{COMMAND_CHANNEL_ID}>!",
                ephemeral=True
            )
            return False
        role = discord.utils.get(interaction.user.roles, name=REQUIRED_ROLE_NAME)
        if role is None:
            await interaction.response.send_message(
                f"❌ You need the '{REQUIRED_ROLE_NAME}' role to submit!",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

@tree.command(
    name="submit",
    description="Submit your art to the art submissions channel!",
    guild=discord.Object(id=GUILD_ID)
)
@can_use_submit()
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
    await channel.send(embed=embed, file=await file.to_file())

    await interaction.response.send_message(
        embed=discord.Embed(
            description=f"✅ Your submission has been sent to <#{ART_SUBMISSIONS_CHANNEL_ID}>!",
            color=0x57F287
        ),
        ephemeral=True
    )

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Bot is online as {client.user}")

client.run(TOKEN)