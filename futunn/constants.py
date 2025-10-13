"""
Constants for Futunn API

Market types, rank types, and other configuration constants.
"""

# Market Types
MARKET_TYPE_US = 2
MARKET_TYPE_HK = 1
MARKET_TYPE_CN = 3

# Plate Types
PLATE_TYPE_ALL = 1

# Rank Types
RANK_TYPE_TOP_TURNOVER = 5
RANK_TYPE_TOP_GAINERS = 1
RANK_TYPE_TOP_LOSERS = 2
RANK_TYPE_TOP_VOLUME = 3
RANK_TYPE_TOP_AMPLITUDE = 4

# Default Configuration
DEFAULT_PAGE_SIZE = 50
DEFAULT_TIMEOUT = 10
DEFAULT_CONCURRENCY_LIMIT = 5

# User Agent
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36"
)

# API Response Codes
SUCCESS_CODE = 0
ERROR_CODE = -1
