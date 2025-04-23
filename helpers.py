import pandas as pd
import os
import urllib.parse
import io
from datetime import datetime
from util import is_data_available
from pandas.api.types import CategoricalDtype
import requests

api_key = os.getenv("ALPHAVANTAGE_KEY", "default_api_key")

base_url = "https://www.alphavantage.co/query"
function = "HISTORICAL_OPTIONS"

right = CategoricalDtype(categories=["put", "call"], ordered=False)

columns = {
    "contractID": str,
    "symbol": str,
    "expiration": str,
    "strike": float,
    "type": right,
    "last": float,
    "mark": float,
    "bid": float,
    "bid_size": int,
    "ask": float,
    "ask_size": int,
    "volume": int,
    "open_interest": int,
    "implied_volatility": float,
    "delta": float,
    "gamma": float,
    "theta": float,
    "vega": float,
    "rho": float,
}

na_values = ["", " ", "N/A", "NaN", "nan", "None", None, "null", "-"]


def fetch_open_interest(
    symbol: str,
    date: datetime,
    format="csv",
) -> None | dict:
    if isinstance(date, str):
        raise TypeError("date must be a datetime object, not a string")
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    if not is_data_available(date):
        return None
    date_q = date.strftime("%Y-%m-%d")
    params = {
        "function": function,
        "symbol": symbol,
        "date": date_q,
        "datatype": format,
        "apikey": api_key,
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    response = requests.get(url)
    if response is None:
        return None
    if response.headers["Content-Type"] == "application/json":
        data = response.json()
        information = data.get("Information")
        message = data.get("message")
        error_message = data.get("Error Message")
        if message is not None or error_message is not None or information is not None:
            return None
        df = pd.DataFrame(data["data"], columns=columns)
        df = df.astype(columns, errors="ignore")
        return df

    if format == "csv":
        try:
            df = pd.read_csv(
                io.StringIO(response.text),
                dtype=columns,
                na_values=na_values,
            )
            return df
        except pd.errors.ParserError:
            return None
    return None


def calculate_sum_option_interest(records):
    total_open_interest = records["open_interest"].sum()
    call_open_interest = records[records["type"] == "call"]["open_interest"].sum()
    put_open_interest = records[records["type"] == "put"]["open_interest"].sum()
    return total_open_interest, call_open_interest, put_open_interest
