import random
from typing import Union, Dict

from loguru import logger
from config import ZKS_CONTRACT, ZKS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class ZKSDomain(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(ZKS_CONTRACT, ZKS_ABI)

    async def get_random_name(self):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"[{self.account_id}][{self.address}] Mint {domain_name}.zks domain")

        check_name = await self.contract.functions.available(domain_name).call()

        if check_name:
            return domain_name

        logger.info(f"[{self.account_id}][{self.address}] {domain_name}.zks is unavailable, try another domain")

        await self.get_random_name()

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint ZKS Domain")

        domain_name = await self.get_random_name()

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.register(domain_name, self.address, 1).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
