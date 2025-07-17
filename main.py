import discord, os # type: ignore
from modal import EnrollModal
from dotenv import load_dotenv # type: ignore
from utils import sqlQuery

# Discord
load_dotenv()
token = os.getenv('DC_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    sqlQuery("CREATE TABLE IF NOT EXISTS user_data (userid BIGINT PRIMARY KEY, server_id BIGINT, hobbies VARCHAR[], server_activities VARCHAR[], quirky_fact VARCHAR[], physical_traits VARCHAR[], additional_facts VARCHAR[]);")
    print("The tables have been created")
    await tree.sync()

@tree.command(name="enroll", description="Allow yourself to be guessed")
async def enroll(interaction: discord.Interaction):
    modal = EnrollModal(title="Oracle Bot Enrollment")
    await interaction.response.send_modal(modal)

@tree.command(name="forgetme", description="Forget everything about you")
async def forget(interaction: discord.Interaction):
    deleted = sqlQuery("DELETE FROM user_data WHERE userid = %s RETURNING *;", (interaction.user.id,), fetch=1)
    if not deleted:
        await interaction.response.send_message("You are not enrolled", ephemeral=True)
        return
    await interaction.response.send_message("Your data has been removed", ephemeral=True)

@tree.command(name="ping", description="Check if the bot is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)
bot.run(token=token)