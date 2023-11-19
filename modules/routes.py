import random
from typing import Union

from loguru import logger
from utils.sleeping import sleep
from .account import Account


class Routes(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy

    def process_module(self, module):
        if isinstance(module, list):
            return self.process_module(random.choice(module))
        elif isinstance(module, tuple):
            return [self.process_module(module[0]) for _ in range(random.randint(module[1], module[2]))]
        else:
            return module

    def run_modules(self, use_modules):
        modules_to_run = []
        for module in use_modules:
            result = self.process_module(module)
            if isinstance(result, list):
                modules_to_run.extend(result)
            else:
                modules_to_run.append(result)
        return modules_to_run

    async def start(self, use_modules: list, sleep_from: int, sleep_to: int, random_module: bool):
        logger.info(f"[{self.account_id}][{self.address}] Start using routes")

        run_modules = self.run_modules(use_modules)

        if random_module:
            random.shuffle(run_modules)

        for module in run_modules:
            if module is None:
                logger.info(f"[{self.account_id}][{self.address}] Skip module")
                continue

            await module(self.account_id, self.private_key, self.proxy)

            await sleep(sleep_from, sleep_to)
