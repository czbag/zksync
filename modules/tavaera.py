import random
from typing import Union

from loguru import logger
from web3 import Web3

from config import TAVAERA_CONTRACT, TAVAERA_ID_CONTRACT, TAVAERA_ABI, TAVAERA_ID_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Tavaera(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def mint_id(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Tavaera ID")

        contract = self.get_contract(TAVAERA_ID_CONTRACT, TAVAERA_ID_ABI)

        self.tx.update({"value": Web3.to_wei(0.0003, "ether")})

        transaction = contract.functions.mintCitizenId().build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    def mint_nft(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Tavaera NFT")

        contract = self.get_contract(TAVAERA_CONTRACT, TAVAERA_ABI)

        self.tx.update({"value": 0})
        self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        transaction = contract.functions.mint().build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    def mint(self, sleep_from: int, sleep_to: int):
        self.mint_id()

        sleep(sleep_from, sleep_to)

        self.mint_nft()
