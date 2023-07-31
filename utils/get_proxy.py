import random
import sys

from loguru import logger

from config import PROXIES, RPC
from web3 import Web3


def check_proxy(proxy):
    request_kwargs = {}
    if proxy:
        request_kwargs = {"proxies": {"https": f"http://{proxy}"}}

    w3 = Web3(Web3.HTTPProvider(random.choice(RPC["ethereum"]["rpc"]), request_kwargs=request_kwargs))
    if w3.is_connected():
        return True
    else:
        return False


def get_proxy():
    try:
        proxy = random.choice(PROXIES)
        logger.info(f"Trying to connect to the proxy [{proxy}]")
        result = check_proxy(proxy)
        if result:
            logger.success(f"Proxy [{proxy}] is available")
            return proxy
        else:
            logger.error(f"Proxy [{proxy}] is unavailable, try another proxy")
            PROXIES.remove(proxy)
            get_proxy()
    except IndexError:
        logger.error("Not found proxy")
        sys.exit()
