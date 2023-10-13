import asyncio
import random

from loguru import logger


async def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)

    logger.info(f"💤 Sleep {delay} s.")
    for _ in range(delay):
        await asyncio.sleep(1)
