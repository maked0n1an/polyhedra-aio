import time
import random
import asyncio

from input_data.config import *
from loguru import logger


async def sleep_initial_indicator(address):
    secs = random.randint(INITIAL_DELAY[0], INITIAL_DELAY[1])
    logger.info(f'{address}: - пауза в виде {secs} секунд...')
    await asyncio.sleep(secs)