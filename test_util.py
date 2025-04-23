from datetime import datetime
from util import get_next_option_expiry, get_previous_trading_date


def test_get_next_option_expiry():
    # Monday before expiration
    today = datetime(2025, 3, 17)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 3, 21)

    # Day before expiration
    today = datetime(2025, 3, 20)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 3, 21)

    # Day of expiration
    today = datetime(2025, 3, 21)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 3, 21)

    # Day after expiration
    today = datetime(2025, 3, 22)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 3, 28)

    # Test when the next friday is a holiday
    today = datetime(2025, 4, 16)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 4, 17)

    # Day of expiration when friday is a holiday
    today = datetime(2025, 4, 17)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 4, 17)

    # Day after expiration when friday is a holiday
    today = datetime(2025, 4, 18)
    result = get_next_option_expiry(today)
    assert result == datetime(2025, 4, 25)


def test_get_previous_trading_date():
    # Monday
    today = datetime(2025, 3, 17)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 3, 14)

    # Friday
    today = datetime(2025, 3, 21)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 3, 20)

    # Saturday
    today = datetime(2025, 3, 22)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 3, 21)

    # Sunday
    today = datetime(2025, 3, 23)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 3, 21)

    # Friday is a holiday
    today = datetime(2025, 4, 18)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 4, 17)

    # Friday is a holiday
    today = datetime(2025, 4, 19)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 4, 17)

    # Previous Friday is a holiday
    today = datetime(2025, 4, 21)
    result = get_previous_trading_date(today)
    assert result == datetime(2025, 4, 17)
