from config.config import BASE_URL
from utils.achievement import CONSOLE_NAME_MAP
from utils.datetime import calculate_time_difference

class Game:
    """
    A class to represent a Game.
    """
    def __init__(self, data: dict):
        """
        Constructs all the necessary attributes for the Game object.

        Args:
            data (dict): The data dictionary containing all the game details.
        """
        self.achievement_set_version_hash = data.get('achievement_set_version_hash', "N/A")
        self.achievements = {}
        achievements_data = data.get('Achievements', {})
        for id, achievement_data in achievements_data.items():
            self.achievements[achievement_data['Title']] = achievement_data
        self.console_id = data.get('ConsoleID', "N/A")
        self.console_name = data.get('ConsoleName', "N/A")
        self.developer = data.get('Developer', "N/A")
        self.flags = data.get('Flags', "N/A")
        self.forum_topic_id = data.get('ForumTopicID', "N/A")
        self.genre = data.get('Genre', "N/A")
        self.guideurl = data.get('GuideURL', "No guide available")
        self.id = data.get('ID', "N/A")
        self.image_boxart = f"{BASE_URL}{data.get('ImageBoxArt', '')}"
        self.image_icon = f"{BASE_URL}{data.get('ImageIcon', '')}"
        self.image_ingame = f"{BASE_URL}{data.get('ImageIngame', '')}"
        self.image_title = data.get('ImageTitle', "N/A")
        self.isfinal = data.get('IsFinal', "N/A")
        self.parent_game_id = data.get('ParentGameID', "N/A")
        self.publisher = data.get('Publisher', "N/A")
        self.released = data.get('Released', "N/A")
        self.richpresence = data.get('RichPresencePatch', "N/A")
        self.title = data.get('Title', "N/A")
        self.total_achievements = data.get('NumAchievements', "N/A")
        self.total_achievements_earned_hardcore = data.get('NumAwardedToUserHardcore', "N/A")
        self.total_achievements_earned_softcore = data.get('NumAwardedToUser', "N/A")
        self.total_players_hardcore = data.get('NumDistinctPlayersHardcore', "N/A")
        self.total_players_softcore = data.get('NumDistinctPlayersCasual', "N/A")
        self.total_points = data.get('points_total', "N/A")
        self.updated = data.get('Updated', "N/A")
        self.url = f"{BASE_URL}/game/{self.id}" if self.id != "N/A" else "N/A"
        self.user_completion_hardcore = data.get('UserCompletionHardcore', "N/A")

    def is_completed(self) -> bool:
        """
        Checks if the game is completed by the user.

        Returns:
            bool: True if the game is completed, False otherwise.
        """
        return self.user_completion_hardcore == "100.00%"
    
    def remap_console_name(self) -> str:
        """
        Remaps the console name to its abbreviation.

        Returns:
            str: The abbreviation of the console name if it exists in the map, otherwise the original console name.
        """
        return CONSOLE_NAME_MAP.get(self.console_name, self.console_name)
    
    def days_since_last_achievement(self) -> str:
        """
        Calculate the time passed between the first and last hardcore achievement earned by the user.

        Returns:
            str: A string representing the time passed between the first and last hardcore achievement.
        """
        if dates := [
            achievement_data.get('DateEarnedHardcore')
            for achievement_data in self.achievements.values()
            if achievement_data.get('DateEarnedHardcore')
        ]:
            earliest, latest = min(dates), max(dates)
            return calculate_time_difference(earliest, latest)
        else:
            return "No hardcore achievements earned"

    def calculate_total_true_ratio(self) -> str:
        """
        Calculates the total TrueRatio for all achievements.

        Returns:
            str: The total TrueRatio for all achievements, formatted with points.
        """
        total_true_ratio = sum(achievement_data.get('TrueRatio', 0) for achievement_data in self.achievements.values())
        return f"{total_true_ratio:,}".replace(',', '.')

class UnlockDistribution:
    """
    A call to this endpoint will retrieve a dictionary 
    of the number of players who have earned a specific number of achievements 
    for a given game ID. This endpoint can be used to determine 
    the total mastery count for a game, as well as how rare that overall mastery is.
    """
    def __init__(self, data):
        """
        Initializes the UnlockDistribution object.

        Args:
            data: The data for the UnlockDistribution object.
        """
        self.data = data

    def get_highest_unlock(self):
        """
        Returns the highest unlock value from the data.

        Returns:
            The highest unlock value or None.
        """
        sorted_keys = sorted(self.data, key=int, reverse=True)  # Sort keys as integers in descending order
        highest_unlock_key = next((key for key in sorted_keys if self.data[key] != 0), None)
        return self.data[highest_unlock_key] if highest_unlock_key is not None else None