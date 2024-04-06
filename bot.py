import discord
from discord.ext import tasks
import asyncio

from achievements import process_achievements
from daily_overview import process_daily_overview
from utils import delay_until_next_15th_minute, delay_until_next_midnight

from config import token, users, api_key, api_username, ACHIEVEMENTS_CHANNEL_ID, DAILY_OVERVIEW_CHANNEL_ID

from custom_logger import logger

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')
    tasks = [
        ("Achievements", delay_until_next_15th_minute, process_achievements_task),
        ("Daily Overview", delay_until_next_midnight, process_daily_overview_task),
    ]

    for task_name, delay_func, task in tasks:
        logger.info(f"Preparing to create {task_name} task")
        try:
            delay = delay_func()
        except Exception as e:
            logger.error(f"Error calculating delay for {task_name} task: {e}")
        else:
            asyncio.create_task(start_task_after_delay(delay, task, task_name))
            logger.info(f"{task_name} task created")

async def start_task_after_delay(delay, task, task_name):
    logger.info(f"Waiting for {delay} seconds before starting task {task_name}")
    await asyncio.sleep(delay)
    try:
        task.start()
    except Exception as e:
        logger.error(f"Error starting task {task_name}: {e}")

@tasks.loop(minutes=15)
async def process_achievements_task():
    channel = client.get_channel(ACHIEVEMENTS_CHANNEL_ID)
    try:
        await process_achievements(users, api_username, api_key, channel)
    except Exception as e:
        logger.error(f'Error processing achievements: {e}')

@tasks.loop(hours=24)
async def process_daily_overview_task():
    channel = client.get_channel(DAILY_OVERVIEW_CHANNEL_ID)
    try:
        await process_daily_overview(users, api_username, api_key, channel)
    except Exception as e:
        logger.error(f'Error processing daily overview: {e}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(token)