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

        self.user = data.get('User') or "N/A"
        self.user_pic = f"{BASE_URL}{data.get('UserPic', '')}"
        self.user_pic_unique = f"{self.user_pic}?timestamp={int(time.time())}"
        self.member_since = data.get('MemberSince') or "N/A"
        self.rich_presence_msg = data.get('RichPresenceMsg') or "N/A"
        self.last_game_id = data.get('LastGameID') or "N/A"
        self.contrib_count = data.get('ContribCount', 0)
        self.contrib_yield = data.get('ContribYield', 0)
        self.total_points = data.get('TotalPoints', 0)
        self.total_points_format = format(self.total_points, ',').replace(',', '.') if self.total_points >= 10000 else self.total_points
        self.total_softcore_points = data.get('TotalSoftcorePoints', 0)
        self.total_true_points = data.get('TotalTruePoints', 0)
        self.total_true_points_format = format(self.total_true_points, ',').replace(',', '.') if self.total_true_points >= 10000 else str(self.total_true_points)
        self.permissions = data.get('Permissions') or "N/A"
        self.untracked = data.get('Untracked') or "N/A"
        self.id = data.get('ID') or "N/A"
        self.user_wall_active = data.get('UserWallActive') or "N/A"
        self.motto = data.get('Motto') or "N/A"