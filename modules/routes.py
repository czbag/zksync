import random

from loguru import logger
from utils.sleeping import sleep
from .account import Account


class Routes(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy

    def start(self, use_modules: list, sleep_from: int, sleep_to: int, random_module: bool):
        logger.info(f"[{self.address}] Start using routes")

        for _ in range(0, len(use_modules)):
            if random_module:
                module = random.choice(use_modules)
                module(self.private_key, self.proxy)
                use_modules.remove(module)
            else:
                use_modules[_](self.private_key, self.proxy)
            sleep(sleep_from, sleep_to)
