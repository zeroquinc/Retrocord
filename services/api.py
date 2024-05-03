import requests
from typing import List

from config.config import RETROACHIEVEMENTS_INTERVAL, BASE_URL
from utils.custom_logger import logger

from services.profile import Profile
from services.game import Game, UnlockDistribution
from services.achievement import Achievement
from services.progress import Progress

class BaseAPI:
    """
    BaseAPI: Base class for API requests

    Explanation:
    Handles the base functionality for making API requests.

    Args:
    - endpoint: The API endpoint to request data from.
    - params: A dictionary of parameters to include in the request.

    Returns:
    - dict: The JSON response data from the API.
    """
    BASE_API_URL = f"{BASE_URL}/API/"

    def __init__(self, endpoint: str, params: dict):
        self.endpoint = endpoint
        self.params = params

    def fetch_data(self) -> dict:
        url = f"{self.BASE_API_URL}{self.endpoint}"
        response = requests.get(url, params=self.params)
        response.raise_for_status()
        return response.json()

class GameDetails(BaseAPI):
    """
    GameDetails: Get details about a game

    Explanation:
    Retrieves and processes details about a specific game.

    Args:
    - game_id: The ID of the game to retrieve details for.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.

    Returns:
    - Game: The game details.
    """
    def __init__(self, game_id: str, api_username: str, api_key: str):
        super().__init__("API_GetGameExtended.php", {'z': api_username, 'y': api_key, 'i': game_id})
        logger.debug(f"Fetching game details for game {game_id}")
        data = self.fetch_data()
        truncated_data = str(data)[:1000]  # Convert the data to a string and take the first 1000 characters (because the response is huge)
        logger.debug(f"API response (truncated): {truncated_data}")
        self.game = Game(data)

    def get_game(self) -> Game:
        return self.game

class UserCompletionRecent(BaseAPI):
    """
    UserCompletionRecent

    Explanation:
    Retrieves a user's recent achievements within a specified time interval.

    Args:
    - username: The username of the user.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.

    Returns:
    - List[Achievement]: A list of recent achievements.
    """
    def __init__(self, username: str, api_username: str, api_key: str):
        super().__init__("API_GetUserRecentAchievements.php", {'z': api_username, 'y': api_key, 'u': username, 'm': RETROACHIEVEMENTS_INTERVAL})
        logger.debug(f"Fetching recent data for user {username}")
        data = self.fetch_data()
        logger.debug(f"API response: {data}")
        self.user = username
        self.achievements = [Achievement(item) for item in data]

    def get_achievements(self) -> List[Achievement]:
        return self.achievements

class UserCompletionByDate(BaseAPI):
    """
    UserCompletionByDate

    Explanation:
    Retrieves achievements earned by a user between two specified dates.

    Args:
    - username: The username of the user.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.
    - start_date: The start date for the query.
    - end_date: The end date for the query.

    Returns:
    - List[Achievement]: A list of achievements earned within the specified date range.
    """
    def __init__(self, username: str, api_username: str, api_key: str, start_date: str, end_date: str):
        super().__init__("API_GetAchievementsEarnedBetween.php", {'z': api_username, 'y': api_key, 'u': username, 'f': start_date, 't': end_date})
        logger.debug(f"Fetching data for user {username} between {start_date} and {end_date}")
        data = self.fetch_data()
        logger.debug(f"API response: {data}")
        self.user = username
        self.achievements = [Achievement(item) for item in data]

    def get_achievements(self) -> List[Achievement]:
        return self.achievements

class UserCompletionProgress(BaseAPI):
    """
    UserCompletionProgress

    Explanation:
    Retrieves a user's completion progress.

    Args:
    - username: The username of the user.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.
    - count: The number of progress items to retrieve (default 100).
    - offset: The offset for retrieving progress items (default 0).

    Returns:
    - Progress: The user's completion progress
    """
    def __init__(self, username: str, api_username: str, api_key: str, count: int = 100, offset: int = 0):
        super().__init__("API_GetUserCompletionProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'c': count, 'o': offset})
        logger.debug(f"Fetching progress data for user {username}")
        data = self.fetch_data()
        self.user = username
        self.progress = Progress(data)

    def get_progress(self) -> Progress:
        return self.progress

class UserProgressGameInfo(BaseAPI):
    """
    UserProgressGameInfo

    Explanation:
    Retrieves a user's progress in a specific game.

    Args:
    - game_id: The ID of the game.
    - username: The username of the user.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.

    Returns:
    - Game: The game progress information for the user. 
    """
    def __init__(self, game_id: str, username: str, api_username: str, api_key: str):
        super().__init__("API_GetGameInfoAndUserProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'g': game_id})
        logger.debug(f"Fetching progress data for user {username} in game {game_id}")
        data = self.fetch_data()
        truncated_data = str(data)[:1000]  # Convert the data to a string and take the first 1000 characters (because the response is huge)
        logger.debug(f"API response (truncated): {truncated_data}")
        self.user = username
        self.game = Game(data)

    def get_game(self) -> Game:
        return self.game

class UserProfile(BaseAPI):
    """
    UserProfile

    Explanation:
    Retrieves and processes a user's profile data.

    Args:
    - username: The username of the user.
    - api_username: The API username for authentication.
    - api_key: The API key for authentication.

    Returns:
    - Profile: The user's profile data.
    """
    def __init__(self, username: str, api_username: str, api_key: str):
        super().__init__("API_GetUserProfile.php", {'z': api_username, 'y': api_key, 'u': username})
        logger.debug(f"Fetching profile data for user {username}")
        data = self.fetch_data()
        logger.debug(f"API response: {data}")
        self.profile = Profile(data)

    def get_profile(self) -> Profile:
        return self.profile
    
class GameUnlocks(BaseAPI):
    """
    GameUnlocks

    Explanation:
    Retrieves and processes data related to achievement distribution in a game.

    Args:
    - username: The username of the user.
    - api_key: The API key for authentication.
    - game_id: The ID of the game.

    Returns:
    - UnlockDistribution: The achievement distribution data for the game.
    """
    def __init__(self, username: str, api_key: str, game_id: str):
        super().__init__("API_GetAchievementDistribution.php", {'z': username, 'y': api_key, 'i': game_id, 'h': '1'})
        logger.debug(f"Fetching Achievement Distribution data for game {game_id}")
        data = self.fetch_data()
        logger.debug(f"API response: {data}")
        self.distribution = UnlockDistribution(data)

    def get_distribution(self) -> UnlockDistribution:
        return self.distribution