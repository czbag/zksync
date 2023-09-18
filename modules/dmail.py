import random
from typing import Union

from loguru import logger
from web3 import Web3
from config import DMAIL_ABI, DMAIL_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Dmail(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(DMAIL_CONTRACT, DMAIL_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "to": Web3.to_checksum_address(DMAIL_CONTRACT),
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    @staticmethod
    def get_random_email():
        domain_list = ["@gmail.com", "@dmail.ai"]

        domain_address = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        return domain_address + random.choice(domain_list)

    @retry
    @check_gas
    def send_mail(self, random_receiver: bool):
        logger.info(f"[{self.account_id}][{self.address}] Send email")

        email_address = self.get_random_email() if random_receiver else f"{self.address}@dmail.ai"

        data = self.contract.encodeABI("send_mail", args=(email_address, email_address))

        self.tx.update({"data": data})

        signed_txn = self.sign(self.tx)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
