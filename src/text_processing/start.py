import asyncio

from src.config import PARSING_INTERVAL
from src.text_processing.clustering import run_clustering
from src.text_processing.parsing import run_parsers


async def start_background_task():
    """Запуск приложения каждые period секунд"""
    
    while True:
        # await run_parsers()
        await run_clustering()
        await asyncio.sleep(PARSING_INTERVAL)
