import random
from typing import Union

from loguru import logger
from config import MINTER_ABI, MINTER_CONTRACT
from .account import Account


class Minter(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(MINTER_CONTRACT, MINTER_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gas": random.randint(1000000, 1100000),
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint NFT")

        try:
            transaction = self.contract.functions.mint().build_transaction(self.tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        except Exception as e:
            logger.error(f"[{self.account_id}][{self.address}] Error | {e}")
