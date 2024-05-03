from config.config import BASE_URL
from utils.achievement_utils import CONSOLE_NAME_MAP
from utils.time_utils import calculate_time_difference

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
        attributes = ['achievement_set_version_hash', 'ConsoleID', 'ConsoleName', 'Developer', 'Flags', 'ForumTopicID', 'Genre', 'GuideURL', 'ID', 'ImageTitle', 'IsFinal', 'ParentGameID', 'Publisher', 'Released', 'RichPresencePatch', 'Title', 'NumAchievements', 'NumAwardedToUserHardcore', 'NumDistinctPlayersHardcore', 'NumDistinctPlayersCasual', 'points_total', 'Updated', 'UserCompletionHardcore']
        for attr in attributes:
            setattr(self, attr.lower(), data.get(attr, "N/A"))
        self.achievements = {achievement_data['Title']: achievement_data for achievement_data in data.get('Achievements', {}).values()}
        self.image_boxart = f"{BASE_URL}{data.get('ImageBoxArt', '')}"
        self.image_icon = f"{BASE_URL}{data.get('ImageIcon', '')}"
        self.image_ingame = f"{BASE_URL}{data.get('ImageIngame', '')}"
        self.url = f"{BASE_URL}/game/{self.id}" if self.id != "N/A" else "N/A"

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