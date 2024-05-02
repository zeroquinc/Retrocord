from datetime import datetime
import pytz

from utils.time_utils import ordinal

class Progress:
    def __init__(self, data):
        self.count = data.get('Count')
        self.total = data.get('Total')
        self.results = [Result(result) for result in data.get('Results', [])]

    def __str__(self):
        results_str = ', '.join(str(result) for result in self.results)
        return f'Count: {self.count}, Total: {self.total}, Results: [{results_str}]'
    
    def count_mastered(self):
        count = len([result for result in self.results if result.highest_award_kind == 'mastered'])
        return ordinal(count)

class Result:
    def __init__(self, data):
        self.game_id = data.get('GameID')
        self.title = data.get('Title')
        self.image_icon = data.get('ImageIcon')
        self.console_id = data.get('ConsoleID')
        self.console_name = data.get('ConsoleName')
        self.max_possible = data.get('MaxPossible')
        self.num_awarded = data.get('NumAwarded')
        self.num_awarded_hardcore = data.get('NumAwardedHardcore')
        self.most_recent_awarded_date = data.get('MostRecentAwardedDate')
        self.highest_award_kind = data.get('HighestAwardKind')
        self.highest_award_date = data.get('HighestAwardDate')
        self.highest_award_date_format = self.format_date(self.highest_award_date)

    def __str__(self):
        return f'GameID: {self.game_id}, Title: {self.title}, ImageIcon: {self.image_icon}, ConsoleID: {self.console_id}, ConsoleName: {self.console_name}, MaxPossible: {self.max_possible}, NumAwarded: {self.num_awarded}, NumAwardedHardcore: {self.num_awarded_hardcore}, MostRecentAwardedDate: {self.most_recent_awarded_date}, HighestAwardKind: {self.highest_award_kind}, HighestAwardDate: {self.highest_award_date}'
    
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