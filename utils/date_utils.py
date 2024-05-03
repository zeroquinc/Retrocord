from datetime import datetime
import pytz

def format_date(date: datetime) -> str:
    """
    Formats the date to Amsterdam timezone.

    Parameters
    ----------
    date : datetime
        The date to be formatted.

    Returns
    -------
    str
        The formatted date.
    """
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    date = date.astimezone(amsterdam_tz)
    return date.strftime("%d/%m/%y at %H:%M:%S")