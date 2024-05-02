import discord
import json
from services.api import UserProfile, GameDetails
from utils.custom_logger import logger

async def process_presence(bot, user, api_username, api_key):
    try:
        user_profile = UserProfile(user, api_username, api_key)
        profile = user_profile.get_profile()
        last_game_id = profile.last_game_id

        # Load the game data from the JSON file
        try:
            with open('games.json', 'r') as f:
                games = json.load(f)
        except FileNotFoundError:
            games = {}

        # Check if the game is already in the JSON file
        game_data = games.get(str(last_game_id))

        # If the game is not in the JSON file, fetch it from the API and store it in the JSON file
        if game_data is None:
            logger.info(f"Game ID {last_game_id} not found in JSON. Fetching from API.")
            game_details = GameDetails(last_game_id, api_username, api_key)
            game = game_details.get_game()
            game_title = game.title
            game_platform = game.remap_console_name()
            games[str(last_game_id)] = {"title": game_title, "platform": game_platform}
            with open('games.json', 'w') as f:
                json.dump(games, f, indent=4)
        else:
            logger.info(f"Game ID {last_game_id} found in JSON.")
            game_title = game_data["title"]
            game_platform = game_data["platform"]

        await bot.change_presence(activity=discord.Game(name=f"{game_title} ({game_platform})"))
        logger.info(f"Set bot's rich presence to {game_title} ({game_platform}) for {user}")
    except Exception as e:
        logger.error(f'Error processing user {user}: {e}')