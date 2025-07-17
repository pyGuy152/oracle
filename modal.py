import discord, json
from utils import askAI, sqlQuery

class EnrollModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.TextInput(
            label="Main hobbies/interests?",
            placeholder="e.g., Gaming, Art, Coding, Reading",
            style=discord.TextStyle.paragraph, 
            required=True,
            max_length=500
        ))
        self.add_item(discord.ui.TextInput(
            label="Favorite activites in server?",
            placeholder="e.g., I love talking in #general-chat, I love being in vc and playing roblox",
            style=discord.TextStyle.paragraph, 
            required=True,
            max_length=500
        ))
        self.add_item(discord.ui.TextInput(
            label="Unique or quirky fact about you?",
            placeholder="e.g., I collect vintage action figures, I can juggle 5 balls",
            style=discord.TextStyle.paragraph,
            required=True, 
            max_length=500
        ))
        self.add_item(discord.ui.TextInput(
            label="Physical traits (Optional)?",
            placeholder="e.g., I have blue eyes, I look like gojo",
            style=discord.TextStyle.paragraph, 
            required=False,
            max_length=500
        ))
        self.add_item(discord.ui.TextInput(
            label="Anything else you want to share?",
            placeholder="e.g., I have a girlfriend, I have held a human heart before",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=500
        ))

    async def on_submit(self, interaction: discord.Interaction):
        hobbies = self.children[0].value 
        server_activites = self.children[1].value
        quirky_fact = self.children[2].value
        physical_traits = self.children[3].value
        additional_facts = self.children[4].value
        data = "none"
        for i in range(3):
            try:
                response = askAI(f'Process the following raw user input into a JSON object. The JSON should have the following keys: "hobbies", "server_activities", "quirky_fact", "physical_traits", and "additional_facts". Each key\'s value should be a list of strings. Also only send the json back and try to be general like something others might also have/do. MAKE EVERYTHING LOWERCASE AND ONLY ONE WORD PER ELEMENT IN THE LIST. \n\n Raw user input:\nHobbies: {hobbies}\nserver_activites: {server_activites}\nquirky_fact: {quirky_fact}\nphysical_traits: {physical_traits}\nadditional_facts: {additional_facts}')
                response = response.replace("```json","")
                response = response.replace("``` json", "")
                response = response.replace("```","")
                data = json.loads(response)
            except:
                print(f"Trying again, {i+1} time")
        if data == "none":
            await interaction.response.send_message("Try again later", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="Enrollment Complete!",
            description="Thanks for enrolling! Here's what I gathered:",
            color=discord.Color.green()
        )
        embed.add_field(name="Hobbies/Interests", value=hobbies, inline=False)
        embed.add_field(name="Server Activites", value=server_activites, inline=False)
        embed.add_field(name="Quirky Fact", value=quirky_fact, inline=False)
        if physical_traits:
            embed.add_field(name="Physical Traits", value=physical_traits, inline=False)
        else:
            embed.add_field(name="Physical Traits", value="*(No Traits provided)*", inline=False)
        if additional_facts:
            embed.add_field(name="Additional Facts", value=additional_facts, inline=False)
        else:
            embed.add_field(name="Additional Facts", value="*(No Facts provided)*", inline=False)

        embed.add_field(name="",value="Your data is secure and safe and you can always remove it using the /forgetme command.",inline=False)
        await interaction.response.send_message(embeds=[embed], ephemeral=True)
