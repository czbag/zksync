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
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    @staticmethod
    def generate_collection_data():
        title = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 15)))
        symbol = "".join(random.sample([chr(i) for i in range(65, 91)], random.randint(3, 6)))
        return title, symbol

    @retry
    @check_gas
    def create(self):
        logger.info(f"[{self.account_id}][{self.address}] Create NFT collection on Omnisea")

        title, symbol = self.generate_collection_data()

        transaction = self.contract.functions.create([
            title,
            symbol,
            "",
            "",
            0,
            True,
            0,
            int(time.time()) + 1000000]
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
