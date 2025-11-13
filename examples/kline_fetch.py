import time
import json
import asyncio

from futunn import MARKET_TYPE_US, RANK_TYPE_TOP_TURNOVER, FutunnClient


async def main():
    """Main example function"""

    print("=== Futunn API Client - Basic Usage ===\n")

    # Create client instance
    async with FutunnClient() as client:
        
        params = {
            "stockId": "203290",
            "marketType": "2",
            "type": "2",
            "marketCode": "11",
            "instrumentType": "4",
            "subInstrumentType": "4002",
            "_": str(int(time.time() * 1000))
        }

        # # Fetch stock list
        # data = await client.get_stock_kline(
        #     params=params
        # )
        
        data = await client.get_stock_min_kline(
            params=params
        )

        print(data)


if __name__ == "__main__":
    asyncio.run(main())
