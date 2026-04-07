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

# Role check
def has_required_role():
    async def predicate(interaction: discord.Interaction):
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
@has_required_role()
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
    guild = discord.Object(id=GUILD_ID)
    # Sync the command only for this guild
    await tree.sync(guild=guild)
    print(f"Bot is online as {client.user}")

    # Restrict the command to only COMMAND_CHANNEL_ID
    for command in await tree.fetch_commands(guild=guild):
        if command.name == "submit":
            await command.edit(
                guild=guild,
                default_permission=False
            )

    # Give permission to the channel
    guild_obj = client.get_guild(GUILD_ID)
    if guild_obj:
        channel = guild_obj.get_channel(COMMAND_CHANNEL_ID)
        if channel:
            perms = discord.PermissionOverwrite()
            perms.send_messages = True
            perms.use_application_commands = True
            await channel.set_permissions(guild_obj.default_role, overwrite=None)  # remove default perms
            await channel.set_permissions(guild_obj.get_role(guild_obj.me.top_role.id), overwrite=perms)  # bot perms

client.run(TOKEN)