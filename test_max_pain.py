import pandas as pd
import pytest
from open_interest import calculate_max_pain

open_interest_data = [
    {"expiration": "2024-03-22", "strike": 90, "type": "call", "open_interest": 100},
    {"expiration": "2024-03-15", "strike": 90, "type": "call", "open_interest": 100},
    {"expiration": "2024-03-15", "strike": 90, "type": "put", "open_interest": 50},
    {"expiration": "2024-03-15", "strike": 100, "type": "call", "open_interest": 200},
    {"expiration": "2024-03-15", "strike": 100, "type": "put", "open_interest": 150},
    {"expiration": "2024-03-15", "strike": 110, "type": "call", "open_interest": 50},
    {"expiration": "2024-03-15", "strike": 110, "type": "put", "open_interest": 200},
    {"expiration": "2024-03-15", "strike": 120, "type": "call", "open_interest": 20},
    {"expiration": "2024-03-15", "strike": 120, "type": "put", "open_interest": 300},
    {"expiration": "2024-03-15", "strike": 130, "type": "call", "open_interest": 10},
    {"expiration": "2024-03-15", "strike": 130, "type": "put", "open_interest": 400}
]

def test_calculate_max_pain_with_empty_data():
    """Test that calculate_max_pain returns None for empty data"""
    assert calculate_max_pain(None) is None
    assert calculate_max_pain([]) is None

def test_calculate_max_pain_with_insufficient_data():
    """Test that calculate_max_pain raises ValueError for insufficient data"""
    data = [
        {"expiration": "2024-03-15", "strike": 100, "type": "call", "open_interest": 100},
        {"expiration": "2024-03-15", "strike": 100, "type": "put", "open_interest": 100}
    ]
    with pytest.raises(ValueError, match="Insufficient data to calculate max pain"):
        calculate_max_pain(data)

def test_calculate_max_pain_with_valid_data():
    """Test max pain calculation with valid data"""
    max_pain = calculate_max_pain(open_interest_data)
    assert max_pain == 120

def test_calculate_max_pain_with_dataframe():
    """Test max pain calculation with DataFrame input"""
    df = pd.DataFrame(open_interest_data)
    max_pain = calculate_max_pain(df)
    assert max_pain == 120

def test_calculate_max_pain_with_expiration_date():
    """Test max pain calculation with specific expiration date"""
    max_pain = calculate_max_pain(open_interest_data, expiration_date="2024-03-15")
    assert max_pain == 130

def test_calculate_max_pain_with_invalid_expiration_date():
    """Test max pain calculation with invalid expiration date"""
    with pytest.raises(ValueError, match="No records found for the specified options expiration date"):
        calculate_max_pain(open_interest_data, expiration_date="2024-03-29") 
