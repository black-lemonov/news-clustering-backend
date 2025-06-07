import asyncio

from parsing import run_parsers
from clustering import run_clustering
from config import PARSING_INTERVAL
from aiomultiprocess import Process


async def start_background_task():
    """Запуск приложения каждые period секунд"""
    
    while True:
        # await run_parsers()
        await Process(target=run_clustering)
        await asyncio.sleep(PARSING_INTERVAL)
