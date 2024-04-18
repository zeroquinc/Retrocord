import discord
from discord.ext import commands
from config.config import token
from utils.custom_logger import logger

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    await bot.load_extension('cogs.tasks')

bot.run(token)