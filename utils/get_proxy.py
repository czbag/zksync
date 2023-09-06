import random

from config import RPC
from web3 import Web3


def check_proxy(proxy):
    request_kwargs = {"proxies": {"https": f"http://{proxy}"}}

    w3 = Web3(Web3.HTTPProvider(random.choice(RPC["ethereum"]["rpc"]), request_kwargs=request_kwargs))
    if w3.is_connected():
        return True
    return False
