from loguru import logger
from web3 import Web3
from config import MINTER_ABI, MINTER_CONTRACT
from .account import Account


class Minter(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(Web3.to_checksum_address(MINTER_CONTRACT), MINTER_ABI)

    def mint(self):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gas": 1000000,
            "gasPrice": Web3.to_wei("0.25", "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        transaction = self.contract.functions.mint().build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
