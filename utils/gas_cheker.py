import time
import random

from web3 import Web3
from config import RPC
from settings import MAX_GWEI
from loguru import logger


def get_gas():
    try:
        w3 = Web3(Web3.HTTPProvider(random.choice(RPC["ethereum"]["rpc"])))
        gas_price = w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')

        return gwei
    except Exception as error:
        logger.error(error)


def wait_gas():
    logger.info("Get GWEI")
    while True:
        gas = get_gas()

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            time.sleep(60)
        else:
            break
