import random
from typing import Union

from loguru import logger
from config import ENS_CONTRACT, ENS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class EraDomain(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(ENS_CONTRACT, ENS_ABI)

    async def get_random_name(self):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"[{self.account_id}][{self.address}] Mint {domain_name}.era domain")

        check_name = await self.contract.functions._checkName(domain_name).call()

        if check_name:
            return domain_name

        logger.info(f"[{self.account_id}][{self.address}] {domain_name}.era is unavailable, try another domain")

        await self.get_random_name()

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Era Domain")

        domain_name = await self.get_random_name()
        
        tx_data = await self.get_tx_data(self.w3.to_wei(0.003, "ether"))

        transaction = await self.contract.functions.Register(domain_name).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
