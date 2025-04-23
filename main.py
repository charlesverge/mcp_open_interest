from mcp.server.fastmcp import FastMCP
import logging

from util import get_previous_trading_date
from openinterest import calculate_max_pain
from helpers import (
    fetch_open_interest,
    calculate_sum_option_interest,
)
from datetime import datetime, timedelta
import os
import argparse

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Option Interest",
    "Calculate open interest for a given symbol",
    port=8002,
    debug=True,
    log_level="DEBUG",
)

parser = argparse.ArgumentParser(description="Option Interest MCS Server")
parser.add_argument(
    "--transport",
    choices=["stdio", "sse"],
    default="stdio",
    help="Transport protocol to use (stdio or sse)",
)

args = parser.parse_args()
transport = args.transport


@mcp.tool()
def calculate_option_put_call_sum(symbol: str) -> float:
    """Calculate put call ratio for a given symbol"""
    logger.info(f"Calculating put/call ratio for {symbol}")
    date = get_previous_trading_date(datetime.now())
    open_interest_data = fetch_open_interest(symbol, date)
    total_open_interest, call_open_interest, put_open_interest = (
        calculate_sum_option_interest(open_interest_data)
    )
    put_call_ratio = put_open_interest / call_open_interest
    if put_call_ratio < 1:
        option_sentiment = "bullish"
    else:
        option_sentiment = "bearish"
    description = {
        "total_open_interest": f"Total number of outstanding option contracts: {total_open_interest:,}",
        "call_open_interest": f"Total number of outstanding call options: {call_open_interest:,}",
        "put_open_interest": f"Total number of outstanding put options: {put_open_interest:,}",
        "put_call_ratio": f"Put/Call Ratio: {put_call_ratio:.2f} - Values > 1 indicate more puts than calls",
        "option_sentiment": f"Market Sentiment: {option_sentiment} - Based on whether there are more puts (bullish) or calls (bearish)",
    }

    logger.debug(
        f"Put/call ratio calculation complete for {symbol}: {put_call_ratio:.2f}"
    )
    return {
        "total_open_interest": int(total_open_interest),
        "call_open_interest": int(call_open_interest),
        "put_open_interest": int(put_open_interest),
        "put_call_ratio": float(put_call_ratio),
        "option_sentiment": option_sentiment,
        "description": description,
    }


@mcp.tool()
def calculate_max_pain_for_symbol(symbol: str) -> float:
    """Calculate the max pain for a given symbol"""
    logger.info(f"Calculating max pain for {symbol}")
    try:
        date = (datetime.now() - timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        data = fetch_open_interest(symbol, date)
        if data is None:
            logger.warning(f"No open interest data found for {symbol} on {date}")
            return {"error": f"No open interest data found for {symbol} on {date}"}
        max_pain = calculate_max_pain(data)
        if max_pain is None:
            logger.warning(f"Could not calculate max pain for {symbol}")
            return {"error": f"Could not calculate max pain for {symbol}"}
        logger.debug(f"Max pain calculation complete for {symbol}: {max_pain:.2f}")
        return {
            "max_pain": float(max_pain),
            "description": f"Max Pain: {max_pain:.2f} - The strike price where the maximum loss occurs",
        }
    except ValueError as e:
        logger.error(f"ValueError calculating max pain for {symbol}: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Error calculating max pain for {symbol}: {str(e)}")
        return {"error": f"Error calculating max pain for {symbol}: {str(e)}"}


def main():
    try:
        logger.info("Starting Option Interest MCS...")
        api_key = os.getenv("ALPHAVANTAGE_KEY", "default_api_key")
        if api_key == "default_api_key":
            logger.error(
                "ALPHAVANTAGE_KEY is not set. Please set it in your environment variable with the key 'ALPHAVANTAGE_KEY'"
            )
            exit(1)
        mcp.run(transport=transport)
    except Exception as e:
        logger.error(f"Error running MCS: {str(e)}")


if __name__ == "__main__":
    main()
