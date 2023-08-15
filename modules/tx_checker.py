import random

from loguru import logger
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from eth_account import Account as EthereumAccount
from tabulate import tabulate

from config import ACCOUNTS, RPC


async def check_tx():
    data = {}

    logger.info("Start transaction checker")
    for pk in ACCOUNTS:
        web3 = Web3(
            AsyncHTTPProvider(random.choice(RPC["zksync"]["rpc"])),
            modules={"eth": (AsyncEth,)},
            middlewares=[],
        )
        account = EthereumAccount.from_key(pk)
        nonce = await web3.eth.get_transaction_count(account.address)
        data.update({f"{account.address}": nonce})

    table = [[k + 1, i, data[i]] for k, i in enumerate(data)]
    headers = ["#", "Address", "Nonce"]
    print(tabulate(table, headers, tablefmt="github"))
