import discord, os, asyncio # type: ignore
from modal import EnrollModal, MyView
from dotenv import load_dotenv # type: ignore
from utils import sqlQuery
from collections import Counter

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

@tree.command(name="guess", description="Start the oracle guessing game (Like akinator)")
async def guess(interaction: discord.Interaction):
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel
    await interaction.response.send_message("Ok! Lets start the game! But before we start if you havent used the /enroll command to allow yourself to be guessed, please do so.")
    enrolled_people = sqlQuery("SELECT * FROM user_data WHERE server_id = %s;", (interaction.guild.id,), fetch="all")
    if not enrolled_people:
        await interaction.followup.send("No one is enrolled in this server. Please use the /enroll command to enroll yourself.")
        return
    data = ["hobbies","server_activities","quirky_fact","physical_traits","additional_facts","hobbies","server_activities","quirky_fact","hobbies","server_activities","quirky_fact"]
    for i in data:
        traits = []
        for person in enrolled_people:
            traits += person[i]

            trait_counts = Counter(traits)
            total_people = len(enrolled_people)
            
            if total_people == 1:
                await interaction.followup.send(f"I GUESS <@{enrolled_people[0]['userid']}>")
                return

            best_trait = traits[0][0]
            best_diff = 10000
            
            for trait, count in trait_counts.items():
                percentage = count / total_people
                diff = abs(percentage - 0.5)
                if diff < best_diff:
                    best_diff = diff
                    best_trait = trait
            view = MyView()
            view.add_item(discord.ui.Button(label="Yes", style=discord.ButtonStyle.primary, custom_id=f"yes"))
            view.add_item(discord.ui.Button(label="No", style=discord.ButtonStyle.danger, custom_id=f"no"))
            await interaction.followup.send(f"Does your persons {i} include {best_trait}?", view=view)
            try:
                interaction_response = await bot.wait_for('interaction', timeout=30.0, check=lambda i: i.data['custom_id'].startswith(('yes', 'no')) and i.user == interaction.user)
                if interaction_response.data['custom_id'] == 'yes':
                    for person in enrolled_people:
                        if best_trait not in person[i]:
                            enrolled_people.remove(person)
                elif interaction_response.data['custom_id'] == 'no':
                    for person in enrolled_people:
                        if best_trait in person[i]:
                            enrolled_people.remove(person)
                await interaction_response.response.defer() # no clue what this does but it is needed to prevent the interaction from timing out - says ai
            except asyncio.TimeoutError:
                await interaction.followup.send("You took too long to respond. Please start again.")
                return
    await interaction.followup.send("Im sorry I coudnt guess the person you were thinking about")

bot.run(token=token)