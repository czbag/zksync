import random

from loguru import logger
from web3 import Web3
from config import DMAIL_ABI, DMAIL_CONTRACT
from .account import Account


class Dmail(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(Web3.to_checksum_address(DMAIL_CONTRACT), DMAIL_ABI)

    def send_mail(self):
        logger.info(f"[{self.address}] Send email")

        tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "to": Web3.to_checksum_address(DMAIL_CONTRACT),
            "gas": random.randint(1000000, 1100000),
            "gasPrice": Web3.to_wei("0.25", "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        data = self.contract.encodeABI("send_mail", args=(f"{self.address}@dmail.ai", f"{self.address}@dmail.ai"))
        tx.update({"data": data})

        signed_txn = self.sign(tx)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
