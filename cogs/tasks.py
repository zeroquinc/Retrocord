import asyncio
from discord.ext import tasks, commands
from src.achievements import process_achievements
from src.daily_overview import process_daily_overview
from src.trophies import process_trophies
from src.presence import process_presence
from utils.time_utils import delay_until_next_interval, delay_until_next_midnight
from config.config import users, api_key, api_username, ACHIEVEMENTS_CHANNEL_ID, DAILY_OVERVIEW_CHANNEL_ID, MASTERY_CHANNEL_ID, TROPHIES_CHANNEL_ID, PLATINUM_CHANNEL_ID, RETROACHIEVEMENTS_INTERVAL, PRESENCE_INTERVAL, TROPHIES_INTERVAL, TASK_START_DELAY
from utils.custom_logger import logger

class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot, start_delay: dict = None) -> None:
        self.bot = bot
        self.start_delay = start_delay or {}
        self.process_achievements.start()  # Always start the task when the cog is loaded
        self.process_daily_overview.start()  # Always start the task when the cog is loaded
        self.process_trophies.start()  # Always start the task when the cog is loaded

        # Initialize the current_user_index to 0
        self.users = users
        self.current_user_index = 0
        self.process_presence.start()

    @tasks.loop(minutes=TROPHIES_INTERVAL)
    async def process_trophies(self):
        trophies_channel = self.bot.get_channel(TROPHIES_CHANNEL_ID)
        platinum_channel = self.bot.get_channel(PLATINUM_CHANNEL_ID)
        try:
            await process_trophies(trophies_channel, platinum_channel)
        except Exception as e:
            logger.error(f'Error processing trophies: {e}')

    @process_trophies.before_loop
    async def before_process_trophies(self):
        await self.bot.wait_until_ready()  # Wait until the bot has connected to the discord API
        if self.start_delay.get('process_trophies', False):  # Only delay the start of the task if its value in the start_delay dictionary is True
            delay = delay_until_next_interval('trophies')  # Calculate the delay
            logger.info(f'Waiting {delay} seconds for Trophies task to start')
            await asyncio.sleep(delay)  # Wait for the specified delay

    @tasks.loop(minutes=RETROACHIEVEMENTS_INTERVAL)
    async def process_achievements(self):
        achievements_channel = self.bot.get_channel(ACHIEVEMENTS_CHANNEL_ID)
        mastery_channel = self.bot.get_channel(MASTERY_CHANNEL_ID)
        try:
            await process_achievements(users, api_username, api_key, achievements_channel, mastery_channel)
        except Exception as e:
            logger.error(f'Error processing achievements: {e}')

    @process_achievements.before_loop
    async def before_process_achievements(self):
        await self.bot.wait_until_ready()  # Wait until the bot has connected to the discord API
        if self.start_delay.get('process_achievements', False):  # Only delay the start of the task if its value in the start_delay dictionary is True
            delay = delay_until_next_interval('retro')  # Calculate the delay
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
        if self.start_delay.get('process_daily_overview', False):  # Only delay the start of the task if its value in the start_delay dictionary is True
            delay = delay_until_next_midnight()  # Get the delay until the next midnight
            logger.info(f'Waiting {delay} seconds for Daily Overview task to start')
            await asyncio.sleep(delay)  # Wait for the specified delay

    @tasks.loop(minutes=PRESENCE_INTERVAL)
    async def process_presence(self):
        try:
            user = self.users[self.current_user_index]
            await process_presence(self.bot, user, api_username, api_key)
            self.current_user_index = (self.current_user_index + 1) % len(self.users)
        except Exception as e:
            logger.error(f'Error processing presence: {e}')

    @process_presence.before_loop
    async def before_process_presence(self):
        await self.bot.wait_until_ready()  # Wait until the bot has connected to the discord API
        if self.start_delay.get('process_presence', False):  # Only delay the start of the task if its value in the start_delay dictionary is True
            delay = delay_until_next_interval('presence')  # Get the delay until the next 15th minute
            logger.info(f'Waiting {delay} seconds for Presence task to start')
            await asyncio.sleep(delay)  # Wait for the specified delay

async def setup(bot):
    await bot.add_cog(TasksCog(bot, start_delay=TASK_START_DELAY))