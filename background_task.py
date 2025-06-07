import asyncio

from parsing import run_parsers
from clustering import run_clustering
from config import PARSING_INTERVAL


async def start_background_task():
    """Запуск приложения каждые period секунд"""
    
    while True:
        await run_parsers()
        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(
        #     None,
        #     run_clustering
        # )
        await asyncio.sleep(PARSING_INTERVAL)
