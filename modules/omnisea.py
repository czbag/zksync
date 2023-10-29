import random
import time
from typing import Union

from loguru import logger
from config import OMNISEA_ABI, OMNISEA_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Omnisea(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(OMNISEA_CONTRACT, OMNISEA_ABI)

    @staticmethod
    def generate_collection_data():
        title = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 15)))
        symbol = "".join(random.sample([chr(i) for i in range(65, 91)], random.randint(3, 6)))
        return title, symbol

    @retry
    @check_gas
    async def create(self):
        logger.info(f"[{self.account_id}][{self.address}] Create NFT collection on Omnisea")

        title, symbol = self.generate_collection_data()

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.create([
            title,
            symbol,
            "",
            "",
            0,
            True,
            0,
            int(time.time()) + 1000000]
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
