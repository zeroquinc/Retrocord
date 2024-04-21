from config.config import BASE_URL
import time

class Profile:
    """
    A class to represent a Profile.
    """

    def __init__(self, data: dict):
        """
        Constructs all the necessary attributes for the Game object.

        Parameters
        ----------
        data : dict
            The data dictionary containing all the game details.
        """
        self.user = data.get('User', "N/A")
        self.user_pic = f"{BASE_URL}{data.get('UserPic', '')}"
        self.user_pic_unique = f"{self.user_pic}?timestamp={int(time.time())}"
        self.user_url = f"{BASE_URL}/user/{self.user}"
        self.member_since = data.get('MemberSince', "N/A")
        self.rich_presence_msg = data.get('RichPresenceMsg', "N/A")
        self.last_game_id = data.get('LastGameID', "N/A")
        self.contrib_count = data.get('ContribCount', 0)
        self.contrib_yield = data.get('ContribYield', 0)
        self.total_points = data.get('TotalPoints', 0)
        self.total_points_format = self.format_points(self.total_points)
        self.total_softcore_points = data.get('TotalSoftcorePoints', 0)
        self.total_softcore_points_format = self.format_points(self.total_softcore_points)
        self.total_true_points = data.get('TotalTruePoints', 0)
        self.total_true_points_format = self.format_points(self.total_true_points)
        self.permissions = data.get('Permissions', "N/A")
        self.untracked = data.get('Untracked', "N/A")
        self.id = data.get('ID', "N/A")
        self.user_wall_active = data.get('UserWallActive', "N/A")
        self.motto = data.get('Motto', "N/A")

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