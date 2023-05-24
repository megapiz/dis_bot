import discord
from discord.ext import commands
import openai
from config import TOKEN
from config import OPENAI_API_KEY

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 1110871391970000936 or message.channel.id == 1110957540063326338:
        user_input = message.content
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_input,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        embedVar = discord.Embed(title="Q: " + user_input, color=0x00ff00)
        embedVar.add_field(name="response from chatGPT :", value=response.choices[0].text.strip(), inline=False)
        
        await message.channel.send(embed=embedVar)


    await bot.process_commands(message)

bot.run(TOKEN)