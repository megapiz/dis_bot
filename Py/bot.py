import discord
from discord.ext import commands
import youtube_dl
import asyncio

# Create a bot instance and set the command prefix
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

# Event: Bot is ready and connected to the server
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Command: Play
@bot.command()
async def play(ctx, url):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send('You are not connected to a voice channel.')
        return

    # Connect to the voice channel
    channel = ctx.author.voice.channel
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
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
            voice_client.play(source)
            await ctx.send('Playing: ' + info['title'])
            while voice_client.is_playing():
                await asyncio.sleep(1)
    except Exception as e:
        await ctx.send('An error occurred while playing the audio.')

    # Disconnect from the voice channel
    await voice_client.disconnect()

# Run the bot with your Discord bot token
bot.run('')
