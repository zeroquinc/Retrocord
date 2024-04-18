import requests
from datetime import datetime
import pytz
import time

from config.config import API_INTERVAL
from utils.achievement_utils import CONSOLE_NAME_MAP

BASE_URL = "https://retroachievements.org"

"""
BaseAPI: Base class for API requests
"""

class BaseAPI:
    BASE_API_URL = f"{BASE_URL}/API/"

    def __init__(self, endpoint, params):
        self.endpoint = endpoint
        self.params = params

    def fetch_data(self):
        url = f"{self.BASE_API_URL}{self.endpoint}"
        response = requests.get(url, params=self.params)
        response.raise_for_status()
        data = response.json()
        return data

"""
GameDetails: Get details about a game
"""
class GameDetails(BaseAPI):
    def __init__(self, game_id, api_username, api_key):
        super().__init__("API_GetGameExtended.php", {'z': api_username, 'y': api_key, 'i': game_id})
        data = self.fetch_data()
        self.game = Game(data)
    # Get the game
    def get_game(self):
        return self.game
    
"""
UserCompletionRecent: Get a user's recent achievements, defaults to 15 minutes
"""
    
class UserCompletionRecent(BaseAPI):
    def __init__(self, username, api_username, api_key):
        super().__init__("API_GetUserRecentAchievements.php", {'z': api_username, 'y': api_key, 'u': username, 'm': API_INTERVAL})
        data = self.fetch_data()
        self.user = username
        self.achievements = [Achievement(item) for item in data]
    # Get the recent achievements earned by the user
    def get_achievements(self):
        return self.achievements

"""
UserCompletionByDate: Get achievements earned by a user between two dates
"""

class UserCompletionByDate(BaseAPI):
    def __init__(self, username, api_username, api_key, start_date, end_date):
        super().__init__("API_GetAchievementsEarnedBetween.php", {'z': api_username, 'y': api_key, 'u': username, 'f': start_date, 't': end_date})
        data = self.fetch_data()
        self.user = username
        self.achievements = [Achievement(item) for item in data]

    # Get the achievements earned by the user
    def get_achievements(self):
        return self.achievements
    
"""
UserCompletionProgress: Get a user's completion progress, currently not used because UserProgressGameInfo is used instead and is better
"""

class UserCompletionProgress(BaseAPI):
    def __init__(self, username, api_username, api_key, count=100, offset=0):
        super().__init__("API_GetUserCompletionProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'c': count, 'o': offset})

"""
UserGameProgress: Get a user's progress in a game
"""

class UserProgressGameInfo(BaseAPI):
    def __init__(self, game_id, username, api_username, api_key):
        super().__init__("API_GetGameInfoAndUserProgress.php", {'z': api_username, 'y': api_key, 'u': username, 'g': game_id})
        data = self.fetch_data()
        self.user = username
        self.game = Game(data)
    # Get the game
    def get_game(self):
        return self.game


"""
UserProfile: Get a user's profile
"""

class UserProfile(BaseAPI):
    def __init__(self, username, api_username, api_key):
        super().__init__("API_GetUserProfile.php", {'z': api_username, 'y': api_key, 'u': username})
        data = self.fetch_data()
        self.profile = Profile(data)
    # Get the user's profile
    def get_profile(self):
        return self.profile

class Profile:
    def __init__(self, data):
        self.user = data.get('User') or "N/A"
        self.user_pic = f"{BASE_URL}{data.get('UserPic', '')}"
        self.user_pic_unique = f"{self.user_pic}?timestamp={int(time.time())}"
        self.member_since = data.get('MemberSince') or "N/A"
        self.rich_presence_msg = data.get('RichPresenceMsg') or "N/A"
        self.last_game_id = data.get('LastGameID') or "N/A"
        self.contrib_count = data.get('ContribCount') or "N/A"
        self.contrib_yield = data.get('ContribYield') or "N/A"
        self.total_points = data.get('TotalPoints') or "N/A"
        self.total_points_format = format(self.total_points, ',').replace(',', '.') if self.total_points >= 10000 else self.total_points
        self.total_softcore_points = data.get('TotalSoftcorePoints') or "N/A"
        self.total_true_points = data.get('TotalTruePoints') or "N/A"
        self.total_true_points_format = format(self.total_true_points, ',').replace(',', '.') if self.total_true_points >= 10000 else str(self.total_true_points)
        self.permissions = data.get('Permissions') or "N/A"
        self.untracked = data.get('Untracked') or "N/A"
        self.id = data.get('ID') or "N/A"
        self.user_wall_active = data.get('UserWallActive') or "N/A"
        self.motto = data.get('Motto') or "N/A"

class Game:
    """
    A class to represent a Game.
    """

    def __init__(self, data: dict):
        """
        Constructs all the necessary attributes for the Game object.

        Parameters
        ----------
        data : dict
            The data dictionary containing all the game details.
        """
        self.achievement_set_version_hash = data.get('achievement_set_version_hash') or "N/A"
        self.achievements = {}
        achievements_data = data.get('Achievements') or {}
        for id, achievement_data in achievements_data.items():
            self.achievements[achievement_data['Title']] = achievement_data
        self.console_id = data.get('ConsoleID') or "N/A"
        self.console_name = data.get('ConsoleName') or "N/A"
        self.developer = data.get('Developer') or "N/A"
        self.flags = data.get('Flags') or "N/A"
        self.forum_topic_id = data.get('ForumTopicID') or "N/A"
        self.genre = data.get('Genre') or "N/A"
        self.guideurl = data.get('GuideURL') or "No guide available"
        self.id = data.get('ID') or "N/A"
        self.image_boxart = f"{BASE_URL}{data.get('ImageBoxArt', '')}"
        self.image_icon = f"{BASE_URL}{data.get('ImageIcon', '')}"
        self.image_ingame = f"{BASE_URL}{data.get('ImageIngame', '')}"
        self.image_title = data.get('ImageTitle') or "N/A"
        self.isfinal = data.get('IsFinal') or "N/A"
        self.parent_game_id = data.get('ParentGameID') or "N/A"
        self.publisher = data.get('Publisher') or "N/A"
        self.released = data.get('Released') or "N/A"
        self.richpresence = data.get('RichPresencePatch') or "N/A"
        self.title = data.get('Title') or "N/A"
        self.total_achievements = data.get('NumAchievements') or "N/A"
        self.total_achievements_earned = data.get('NumAwardedToUserHardcore') or "N/A"
        self.total_players_hardcore = data.get('NumDistinctPlayersHardcore') or "N/A"
        self.total_players_softcore = data.get('NumDistinctPlayersCasual') or "N/A"
        self.total_points = data.get('points_total') or "N/A"
        self.updated = data.get('Updated') or "N/A"
        self.url = f"{BASE_URL}/{self.id}" if self.id else "N/A"
        self.user_completion_hardcore = data.get('UserCompletionHardcore', "N/A")

    def is_completed(self):
        """
        Checks if the game is completed by the user.

        Returns
        -------
        bool
            True if the game is completed, False otherwise.
        """
        return self.user_completion_hardcore == "100.00%"
    
    def remap_console_name(self):
            """
            Remaps the console name to its abbreviation.

            Returns
            -------
            str
                The abbreviation of the console name if it exists in the map, otherwise the original console name.
            """
            return CONSOLE_NAME_MAP.get(self.console_name, self.console_name)

class Achievement:
    """
    A class to represent an Achievement.
    """
    def __init__(self, data: dict):
        """
        Constructs all the necessary attributes for the Achievement object.

        Parameters
        ----------
        data : dict
            The data dictionary containing all the achievement details.
        """
        self.achievement_id = data.get('AchievementID') or "N/A"
        self.author = data.get('Author') or "N/A"
        self.badge_name = data.get('BadgeName') or "N/A"
        self.badge_url = f"{BASE_URL}{data.get('BadgeURL', '')}"
        self.console_name = data.get('ConsoleName') or "N/A"
        self.cumul_score = data.get('CumulScore') or "N/A"
        self.date = data.get('Date') or "N/A"
        self.date_amsterdam = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%d/%m/%y at %H:%M:%S") if self.date != "N/A" else "N/A"
        self.description = data.get('Description') or "N/A"
        self.game_icon = f"{BASE_URL}{data.get('GameIcon', '')}"
        self.game_id = data.get('GameID') or "N/A"
        self.game_title = data.get('GameTitle') or "N/A"
        self.game_url = f"{BASE_URL}{data.get('GameURL', '')}"
        self.mode = "Hardcore" if data.get('HardcoreMode', 0) == 1 else "Softcore"
        self.points = data.get('Points') or "N/A"
        self.retropoints = data.get('TrueRatio') or "N/A"
        self.retropoints_format = format(self.retropoints, ',').replace(',', '.') if self.retropoints >= 10000 else str(self.retropoints)
        self.title = data.get('Title') or "N/A"
        self.type = data.get('Type') or "N/A"
        self.url = f"{BASE_URL}/achievement/{self.achievement_id}" if self.achievement_id else "N/A"

    def remap_console_name(self):
            """
            Remaps the console name to its abbreviation.

            Returns
            -------
            str
                The abbreviation of the console name if it exists in the map, otherwise the original console name.
            """
            return CONSOLE_NAME_MAP.get(self.console_name, self.console_name)