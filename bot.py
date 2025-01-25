import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from llm import generate_text

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def prompt(ctx,*,prompt_text: str):
    generated_text = generate_text(prompt=prompt_text)

    await ctx.send(generated_text)

load_dotenv()

bot.run(os.getenv('BOT_TOKEN'))