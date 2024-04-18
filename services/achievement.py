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
        self.achievement_id = data.get('AchievementID', "N/A")
        self.author = data.get('Author', "N/A")
        self.badge_name = data.get('BadgeName', "N/A")
        self.badge_url = f"{BASE_URL}{data.get('BadgeURL', '')}"
        self.console_name = data.get('ConsoleName', "N/A")
        self.cumul_score = data.get('CumulScore', "N/A")
        self.date = data.get('Date', "N/A")
        self.date_amsterdam = self.format_date(self.date) if self.date != "N/A" else "N/A"
        self.description = data.get('Description', "N/A")
        self.game_icon = f"{BASE_URL}{data.get('GameIcon', '')}"
        self.game_id = data.get('GameID', "N/A")
        self.game_title = data.get('GameTitle', "N/A")
        self.game_url = f"{BASE_URL}{data.get('GameURL', '')}"
        self.mode = "Hardcore" if data.get('HardcoreMode', 0) == 1 else "Softcore"
        self.points = data.get('Points', "N/A")
        self.retropoints = data.get('TrueRatio', 0)
        self.retropoints_format = self.format_points(self.retropoints)
        self.title = data.get('Title', "N/A")
        self.type = data.get('Type', "N/A")
        self.url = f"{BASE_URL}/achievement/{self.achievement_id}" if self.achievement_id != "N/A" else "N/A"

    def format_points(self, points: int) -> str:
        """
        Formats the points with commas as thousands separators.

        Parameters
        ----------
        points : int
            The points to be formatted.

        Returns
        -------
        str
            The formatted points.
        """
        return format(points, ',').replace(',', '.') if points >= 10000 else str(points)

    def format_date(self, date: str) -> str:
        """
        Formats the date to Amsterdam timezone.

        Parameters
        ----------
        date : str
            The date to be formatted.

        Returns
        -------
        str
            The formatted date.
        """
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%d/%m/%y at %H:%M:%S")

    def remap_console_name(self) -> str:
            """
            Remaps the console name to its abbreviation.

            Returns
            -------
            str
                The abbreviation of the console name if it exists in the map, otherwise the original console name.
            """
            return CONSOLE_NAME_MAP.get(self.console_name, self.console_name)