from datetime import datetime


class DateTimeHelper:
    """Helper class for datetime formatting."""


    @staticmethod
    def get_readable_datetime(timestamp: float = None) -> str:
        """
        Returns a readable datetime string.
        - If no timestamp is given, uses the current datetime.
        - If a timestamp (seconds since epoch) is given, formats that datetime.
        """
        if timestamp is None:
            dt = datetime.now()
        else:
            dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%A, %B %d, %Y at %I:%M %p")