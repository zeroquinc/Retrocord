from datetime import datetime, timezone
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
    date = date.replace(tzinfo=timezone.utc)
    date = date.astimezone(pytz.timezone('Europe/Amsterdam'))
    return date.strftime("%d/%m/%y at %H:%M:%S")