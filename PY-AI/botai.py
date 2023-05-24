import discord
from discord.ext import commands
import openai
from youtube_dl import YoutubeDL
import os
import asyncio
from config import TOKEN
from config import OPENAI_API_KEY

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
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

    if message.content.startswith('p!'):
        query = message.content[3:]  # Remove the 'p!' prefix

        channel = bot.author.voice.channel
        voice_client = await channel.connect()

        # Download and play the audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        try:
            ydl = YoutubeDL(params=ydl_opts)
            info = ydl.extract_info(url=query,download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
            voice_client.play(source)
            await bot.send('Playing: ' + info['title'])
            while voice_client.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            await bot.send(e)

        # Disconnect from the voice channel
        await voice_client.disconnect()

    await bot.process_commands(message)

bot.run(TOKEN)
