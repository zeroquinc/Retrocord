from datetime import datetime
import pytz

from utils.time_utils import ordinal

class Progress:
    def __init__(self, data):
        self.count, self.total, self.results = data.get('Count'), data.get('Total'), [Result(result) for result in data.get('Results', [])]

    def __str__(self):
        results_str = ', '.join(str(result) for result in self.results)
        return f"""Count: {self.count}, Total: {self.total}, Results: [{results_str}]"""

    def count_mastered(self):
        count = len([result for result in self.results if result.highest_award_kind == 'mastered'])
        return ordinal(count)

class Result:
    def __init__(self, data):
        (self.game_id, self.title, self.image_icon, self.console_id, self.console_name, self.max_possible, 
         self.num_awarded, self.num_awarded_hardcore, self.most_recent_awarded_date, self.highest_award_kind, 
         self.highest_award_date) = (data.get(key) for key in ('GameID', 'Title', 'ImageIcon', 'ConsoleID', 'ConsoleName', 
                                                               'MaxPossible', 'NumAwarded', 'NumAwardedHardcore', 
                                                               'MostRecentAwardedDate', 'HighestAwardKind', 'HighestAwardDate'))
        self.highest_award_date_format = self.format_date(self.highest_award_date)

    def __str__(self):
        return (f"GameID: {self.game_id}, Title: {self.title}, ImageIcon: {self.image_icon}, "
                f"ConsoleID: {self.console_id}, ConsoleName: {self.console_name}, MaxPossible: {self.max_possible}, "
                f"NumAwarded: {self.num_awarded}, NumAwardedHardcore: {self.num_awarded_hardcore}, "
                f"MostRecentAwardedDate: {self.most_recent_awarded_date}, HighestAwardKind: {self.highest_award_kind}, "
                f"HighestAwardDate: {self.highest_award_date}")
    
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
        if date is None:
            return None
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%d/%m/%y at %H:%M:%S")