import random
from typing import Union

from loguru import logger

from config import (
    SYNCSWAP_CONTRACTS,
    MUTE_CONTRACTS,
    SPACEFI_CONTRACTS,
    PANCAKE_CONTRACTS,
    WOOFI_CONTRACTS,
    VELOCORE_CONTRACTS,
    ZKSYNC_TOKENS
)
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class MultiApprove(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

    @retry
    @check_gas
    def start(self, amount: int, sleep_from: int, sleep_to: int):
        contract_list = [
            SYNCSWAP_CONTRACTS["router"],
            MUTE_CONTRACTS["router"],
            SPACEFI_CONTRACTS["router"],
            PANCAKE_CONTRACTS["router"],
            WOOFI_CONTRACTS["router"],
            VELOCORE_CONTRACTS["router"]
        ]
        token_list = list(ZKSYNC_TOKENS)

        random.shuffle(contract_list)
        random.shuffle(token_list)

        for contract_address in contract_list:
            for _, token in enumerate(token_list):
                if token in ["ETH", "WETH"]:
                    continue

                self.approve(amount, ZKSYNC_TOKENS[token], contract_address)

                sleep(sleep_from, sleep_to)
