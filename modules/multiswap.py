import random
from typing import Union

from loguru import logger
from web3 import Web3
from config import ZKSYNC_TOKENS
from modules import *
from utils.sleeping import sleep


class Multiswap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy
        self.swap_modules = {
            "syncswap": SyncSwap,
            "mute": Mute,
            "spacefi": SpaceFi,
            "pancake": Pancake,
            "velocore": Velocore,
            "woofi": WooFi,
            "odos": Odos,
            "zkswap": ZKSwap,
            "xyswap": XYSwap,
            "openocean": OpenOcean,
            "inch": Inch
        }

    def get_swap_module(self, use_dex: list):
        swap_module = random.choice(use_dex)
        return self.swap_modules[swap_module]

    def swap(
            self,
            use_dex: list,
            sleep_from: int,
            sleep_to: int,
            min_swap: int,
            max_swap: int,
            slippage: int,
            random_swap_token: bool,
            min_percent: int,
            max_percent: int
    ):
        quantity_swap = random.randint(min_swap, max_swap)

        if random_swap_token:
            path = [random.choice(["ETH", "USDC"]) for _ in range(0, quantity_swap)]
            if path[0] == "USDC" and self.get_balance(ZKSYNC_TOKENS["USDC"])["balance"] <= 1:
                path[0] = "ETH"
        else:
            path = ["ETH" if _ % 2 == 0 else "USDC" for _ in range(0, quantity_swap)]

        logger.info(f"[{self.account_id}][{self.address}] Start MultiSwap | quantity swaps: {quantity_swap}")

        for _, token in enumerate(path):
            if token == "ETH":
                decimal = 6
                to_token = "USDC"

                balance = self.w3.eth.get_balance(self.address)

                min_amount = float(Web3.from_wei(int(balance / 100 * min_percent), "ether"))
                max_amount = float(Web3.from_wei(int(balance / 100 * max_percent), "ether"))
            else:
                decimal = 18
                to_token = "ETH"

                balance = self.get_balance(ZKSYNC_TOKENS["USDC"])

                min_amount = balance["balance"] if balance["balance"] <= 1 else balance["balance"] / 100 * min_percent
                max_amount = balance["balance"] if balance["balance"] <= 1 else balance["balance"] / 100 * max_percent

            swap_module = self.get_swap_module(use_dex)(self.account_id, self.private_key, self.proxy)
            swap_module.swap(
                token,
                to_token,
                min_amount,
                max_amount,
                decimal,
                slippage,
                False,
                min_percent,
                max_percent
            )

            if _ + 1 != len(path):
                sleep(sleep_from, sleep_to)
