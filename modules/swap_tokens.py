import random
from typing import Union, List

from loguru import logger
from config import ZKSYNC_TOKENS
from modules import *
from utils.sleeping import sleep


class SwapTokens(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy
        self.swap_modules = {
            "syncswap": SyncSwap,
            "mute": Mute,
            "spacefi": SpaceFi,
            "pancake": Pancake,
            "woofi": WooFi,
            "odos": Odos,
            "zkswap": ZKSwap,
            "xyswap": XYSwap,
            "openocean": OpenOcean,
            "inch": Inch,
            "maverick": Maverick,
            "vesync": VeSync
        }

    def get_swap_module(self, use_dex: list):
        swap_module = random.choice(use_dex)
        return self.swap_modules[swap_module]

    async def swap(
            self,
            use_dex: List,
            tokens: List,
            sleep_from: int,
            sleep_to: int,
            slippage: int,
            min_percent: int,
            max_percent: int,
    ):
        random.shuffle(tokens)

        logger.info(f"[{self.account_id}][{self.address}] Start swap tokens")

        for _, token in enumerate(tokens, start=1):
            if token == "ETH":
                continue

            balance = await self.get_balance(ZKSYNC_TOKENS[token])

            if balance["balance_wei"] > 0:
                swap_module = self.get_swap_module(use_dex)(self.account_id, self.private_key, self.proxy)
                await swap_module.swap(
                    token,
                    "ETH",
                    balance["balance"],
                    balance["balance"],
                    balance["decimal"],
                    slippage,
                    True,
                    min_percent,
                    max_percent
                )

            if _ != len(tokens):
                await sleep(sleep_from, sleep_to)
