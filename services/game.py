from config.config import BASE_URL
from utils.achievement_utils import CONSOLE_NAME_MAP

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