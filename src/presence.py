import discord
from services.api import UserProfile, GameDetails
from utils.custom_logger import logger

async def process_presence(bot, user, api_username, api_key):
    try:
        user_profile = UserProfile(user, api_username, api_key)
        profile = user_profile.get_profile()
        last_game_id = profile.last_game_id
        game_details = GameDetails(last_game_id, api_username, api_key)
        game = game_details.get_game()
        game_title = game.title
        await bot.change_presence(activity=discord.Game(name=game_title))
        logger.info(f"Set bot's rich presence to {game_title} for {user}")
    except Exception as e:
        logger.error(f'Error processing user {user}: {e}')