import asyncio
import time
import random

from web3 import Web3
from web3.eth import AsyncEth

from config import RPC
from settings import CHECK_GWEI, MAX_GWEI
from loguru import logger

from utils.sleeping import sleep


async def get_gas():
    try:
        w3 = Web3(
            Web3.AsyncHTTPProvider(random.choice(RPC["ethereum"]["rpc"])),
            modules={"eth": (AsyncEth,)},
        )
        gas_price = await w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')
        return gwei
    except Exception as error:
        logger.error(error)


async def wait_gas():
    logger.info("Get GWEI")
    while True:
        gas = await get_gas()

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            await sleep(60, 90)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {MAX_GWEI}")
            break


def check_gas(func):
    async def _wrapper(*args, **kwargs):
        if CHECK_GWEI:
            await wait_gas()
        return await func(*args, **kwargs)

    return _wrapper
