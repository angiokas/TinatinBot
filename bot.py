import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        await bot.load_extension('cogs.vc')
    except Exception as e:
        print(f"Error loading cog: {e}")

load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))