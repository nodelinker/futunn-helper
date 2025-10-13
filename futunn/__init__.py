"""
Futunn API Client

An asynchronous Python client for Futunn's stock market quote API.
Inspired by the architecture of py-googletrans.

Example:
    >>> import asyncio
    >>> from futunn import FutunnClient
    >>>
    >>> async def main():
    >>>     client = FutunnClient()
    >>>     stock_list = await client.get_stock_list(market_type=2, page_size=10)
    >>>     print(f"Total: {stock_list.pagination.total} stocks")
    >>>
    >>> asyncio.run(main())
"""

from futunn.client import FutunnClient
from futunn.models import Stock, StockList, Pagination
from futunn.constants import (
    MARKET_TYPE_US,
    MARKET_TYPE_HK,
    MARKET_TYPE_CN,
    RANK_TYPE_TOP_TURNOVER,
    RANK_TYPE_TOP_GAINERS,
    RANK_TYPE_TOP_LOSERS,
)

__version__ = "0.1.0"
__author__ = "Futunn Helper Contributors"
__all__ = [
    "FutunnClient",
    "Stock",
    "StockList",
    "Pagination",
    "MARKET_TYPE_US",
    "MARKET_TYPE_HK",
    "MARKET_TYPE_CN",
    "RANK_TYPE_TOP_TURNOVER",
    "RANK_TYPE_TOP_GAINERS",
    "RANK_TYPE_TOP_LOSERS",
]
