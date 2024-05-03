import discord
import json
from services.api import UserProfile, GameDetails
from utils.custom_logger import logger

async def process_presence(bot, user, api_username, api_key):
    """Process the presence of a user in Discord by setting their rich presence based on the last game they played.

    Args:
        bot: The Discord bot instance.
        user: The user for whom the presence is being processed.
        api_username: The API username for fetching user data.
        api_key: The API key for authentication.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the processing.

    Examples:
        await process_presence(bot_instance, user_instance, 'api_username', 'api_key')
    """
    try:
        user_profile = UserProfile(user, api_username, api_key)
        profile = user_profile.get_profile()
        last_game_id = profile.last_game_id

        def get_or_fetch_game(game_id):
            try:
                with open('games.json', 'r') as f:
                    games = json.load(f)
            except FileNotFoundError:
                games = {}

            if str(game_id) not in games:
                logger.info(f"Fetching game ID {game_id} from API.")
                game_details = GameDetails(game_id, api_username, api_key)
                game = game_details.get_game()
                games[str(game_id)] = {"title": game.title, "platform": game.remap_console_name()}
                with open('games.json', 'w') as f:
                    json.dump(games, f, indent=4)
            else:
                logger.info(f"Game ID {game_id} found in JSON.")
            return games[str(game_id)]

        game_data = get_or_fetch_game(last_game_id)
        game_title = game_data["title"]
        game_platform = game_data["platform"]

        await bot.change_presence(activity=discord.Game(name=f"{game_title} ({game_platform})"))
        logger.info(f"Setting rich presence for {user} to {game_title} ({game_platform})")
    except Exception as e:
        logger.error(f'Error processing user {user}: {e}')