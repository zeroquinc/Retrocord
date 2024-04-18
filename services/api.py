import requests
from typing import List, Optional

from config.config import API_INTERVAL, BASE_URL

from services.profile import Profile
from services.game import Game
from services.achievement import Achievement

"""
BaseAPI: Base class for API requests
"""

class BaseAPI:
    BASE_API_URL = f"{BASE_URL}/API/"

    def __init__(self, endpoint: str, params: dict):
        self.endpoint = endpoint
        self.params = params

    def fetch_data(self) -> dict:
        url = f"{self.BASE_API_URL}{self.endpoint}"
        response = requests.get(url, params=self.params)
        response.raise_for_status()
        data = response.json()
        return data

"""
GameDetails: Get details about a game
"""
class GameDetails(BaseAPI):
    def __init__(self, game_id: str, api_username: str, api_key: str):
        super().__init__("API_GetGameExtended.php", {'z': api_username, 'y': api_key, 'i': game_id})
        data = self.fetch_data()
        self.game = Game(data)

    def get_game(self) -> Game:
        return self.game

"""
UserCompletionRecent: Get a user's recent achievements, defaults to 15 minutes
"""

class UserCompletionRecent(BaseAPI):
    def __init__(self, username: str, api_username: str, api_key: str):
        super().__init__("API_GetUserRecentAchievements.php", {'z': api_username, 'y': api_key, 'u': username, 'm': API_INTERVAL})
        data = self.fetch_data()
        self.user = username
        self.achievements = [Achievement(item) for item in data]

    def get_achievements(self) -> List[Achievement]:
        return self.achievements

"""
UserCompletionByDate: Get achievements earned by a user between two dates
"""

class UserCompletionByDate(BaseAPI):
    def __init__(self, username: str, api_username: str, api_key: str, start_date: str, end_date: str):
        super().__init__("API_GetAchievementsEarnedBetween.php", {'z': api_username, 'y': api_key, 'u': username, 'f': start_date, 't': end_date})
        data = self.fetch_data()
        self.user = username
        self.achievements = [Achievement(item) for item in data]

    def get_achievements(self) -> List[Achievement]:
        return self.achievements

"""
UserCompletionProgress: Get a user's completion progress, currently not used because UserProgressGameInfo is used instead and is better
"""

class UserCompletionProgress(BaseAPI):
    def __init__(self, username: str, api_username: str, api_key: str, count: int = 100, offset: int = 0):
        super().__init__("API_GetUserCompletionProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'c': count, 'o': offset})

"""
UserGameProgress: Get a user's progress in a game
"""

class UserProgressGameInfo(BaseAPI):
    def __init__(self, game_id: str, username: str, api_username: str, api_key: str):
        super().__init__("API_GetGameInfoAndUserProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'g': game_id})
        data = self.fetch_data()
        self.user = username
        self.game = Game(data)

    def get_game(self) -> Game:
        return self.game

"""
UserProfile: Get a user's profile
"""

class UserProfile(BaseAPI):
    def __init__(self, username: str, api_username: str, api_key: str):
        super().__init__("API_GetUserProfile.php", {'z': api_username, 'y': api_key, 'u': username})
        data = self.fetch_data()
        self.profile = Profile(data)

    def get_profile(self) -> Profile:
        return self.profile