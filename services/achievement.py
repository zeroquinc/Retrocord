from config.config import BASE_URL
from datetime import datetime
import pytz
from utils.achievement_utils import CONSOLE_NAME_MAP

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