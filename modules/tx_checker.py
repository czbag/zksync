import asyncio
import random

from eth_typing import ChecksumAddress
from loguru import logger
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from eth_account import Account as EthereumAccount
from tabulate import tabulate

from config import ACCOUNTS, RPC


async def get_nonce(address: ChecksumAddress):
    web3 = Web3(
        AsyncHTTPProvider(random.choice(RPC["zksync"]["rpc"])),
        modules={"eth": (AsyncEth,)},
        middlewares=[],
    )

    nonce = await web3.eth.get_transaction_count(address)

    return nonce


async def check_tx():
    tasks = []

    logger.info("Start transaction checker")

    for _id, pk in enumerate(ACCOUNTS, start=1):
        account = EthereumAccount.from_key(pk)

        tasks.append(asyncio.create_task(get_nonce(account.address), name=account.address))

    await asyncio.gather(*tasks)

    table = [[k, i.get_name(), i.result()] for k, i in enumerate(tasks, start=1)]

    headers = ["#", "Address", "Nonce"]

    print(tabulate(table, headers, tablefmt="github"))
