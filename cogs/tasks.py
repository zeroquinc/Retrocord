import asyncio
from discord.ext import tasks, commands
from src.achievements import process_achievements
from src.daily_overview import process_daily_overview
from utils.time_utils import delay_until_next_15th_minute, delay_until_next_midnight
from config.config import users, api_key, api_username, ACHIEVEMENTS_CHANNEL_ID, DAILY_OVERVIEW_CHANNEL_ID
from utils.custom_logger import logger

class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot, delay_start: bool = True) -> None:
        self.bot = bot
        self.delay_start = delay_start
        self.process_achievements.start()  # Start the task when the cog is loaded
        self.process_daily_overview.start()  # Start the task when the cog is loaded

    @tasks.loop(minutes=15)
    async def process_achievements(self):
        channel = self.bot.get_channel(ACHIEVEMENTS_CHANNEL_ID)
        try:
            await process_achievements(users, api_username, api_key, channel)
        except Exception as e:
            logger.error(f'Error processing achievements: {e}')

    @process_achievements.before_loop
    async def before_process_achievements(self):
        await self.bot.wait_until_ready()  # Wait until the bot has connected to the discord API
        if self.delay_start:
            delay = delay_until_next_15th_minute()  # Get the delay until the next 15th minute
            logger.info(f'Waiting {delay} seconds for Achievements task to start')
            await asyncio.sleep(delay)  # Wait for the specified delay

    @tasks.loop(hours=24)
    async def process_daily_overview(self):
        channel = self.bot.get_channel(DAILY_OVERVIEW_CHANNEL_ID)
        try:
            await process_daily_overview(users, api_username, api_key, channel)
        except Exception as e:
            logger.error(f'Error processing daily overview: {e}')

    @process_daily_overview.before_loop
    async def before_process_daily_overview(self):
        await self.bot.wait_until_ready()  # Wait until the bot has connected to the discord API
        if self.delay_start:
            delay = delay_until_next_midnight()  # Get the delay until the next midnight
            logger.info(f'Waiting {delay} seconds for Daily Overview task to start')
            await asyncio.sleep(delay)  # Wait for the specified delay

async def setup(bot):
    await bot.add_cog(TasksCog(bot, delay_start=True)) # Change to False for debugging