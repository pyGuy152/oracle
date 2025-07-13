import asyncio
import discord, os
from modal import EnrollModal
from dotenv import load_dotenv

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
    await tree.sync()

@tree.command(name="enroll", description="Allow yourself to be guessed")
async def enroll(interaction: discord.Interaction):
    modal = EnrollModal(title="Oracle Bot Enrollment")
    await interaction.response.send_modal(modal)


bot.run(token=token)