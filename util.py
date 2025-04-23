import pandas_market_calendars as mcal
from datetime import timedelta, datetime

# Get NYSE calendar
calendar = mcal.get_calendar("NYSE")

def get_previous_trading_date(date):
    """
    Get the previous trading date for a given date
    
    Args:
        date (datetime): The date to find the previous trading date for
        
    Returns:
        datetime: The previous trading date
    """
    schedule = calendar.schedule(
        start_date=date - timedelta(7), end_date=date - timedelta(1)
    )
    return schedule.index[-1]

def get_next_option_expiry(date):
    """
    Get the next option expiry date for a given date. Options typically expire on Fridays,
    but if Friday is a holiday, they expire on the last trading day before Friday.
    
    Args:
        date (datetime): The date to find the next option expiry for
        
    Returns:
        datetime: The next option expiry date, or None if no valid expiry date found
    """
    # This weeks schedule.
    schedule = calendar.schedule(
        start_date=date, end_date=date + timedelta(6 - date.weekday())
    )
    if not schedule.empty:
        last = schedule.index[-1]
        if last >= date:
            return last
    # Next weeks schedule.
    schedule = calendar.schedule(
        start_date=date, end_date=date + timedelta(6 - date.weekday() + 7)
    )
    if not schedule.empty:
        last = schedule.index[-1]
        if last >= date:
            return last
    return None

def is_market_open(date, exchange="XNYS"):
    """
    Check if the market is open on a given date for a specific exchange
    
    Args:
        date (datetime): The date to check
        exchange (str): The exchange code to check (default: "XNYS" for NYSE)
        
    Returns:
        bool: True if market is open on that date, False otherwise
    """
    calendar = mcal.get_calendar(exchange)
    schedule = calendar.schedule(start_date=date, end_date=date)
    return not schedule.empty

def is_data_available(date_t):
    """
    Check if market data is available for a given date
    
    Args:
        date_t (datetime): The date to check for data availability
        
    Returns:
        bool: True if data should be available, False otherwise
        
    Raises:
        TypeError: If date_t is a string instead of a datetime object
        
    Notes:
        - Data is not available for weekends
        - Data is not available for the current day
        - Data is only available for market open days
    """
    if isinstance(date_t, str):
        raise TypeError("date must be a datetime object, not a string")
    date_t = date_t.replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Data is not available for weekends or today.
    if date_t >= now or date_t.weekday() >= 5:
        return False
    return is_market_open(date_t)
