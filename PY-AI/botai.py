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
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('ai!'):
        user_input = message.content[4:]  # Remove the '!' prefix
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
        await message.channel.send(response.choices[0].text.strip())


    await bot.process_commands(message)

bot.run(TOKEN)