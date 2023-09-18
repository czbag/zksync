import random
from typing import Union

from loguru import logger
from config import ZKS_CONTRACT, ZKS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class ZKSDomain(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(ZKS_CONTRACT, ZKS_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def get_random_name(self):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"[{self.account_id}][{self.address}] Mint {domain_name}.zks domain")

        check_name = self.contract.functions.available(domain_name).call()

        if check_name:
            return domain_name

        logger.info(f"[{self.account_id}][{self.address}] {domain_name}.zks is unavailable, try another domain")

        self.get_random_name()

    @retry
    @check_gas
    def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint ZKS Domain")

        domain_name = self.get_random_name()

        transaction = self.contract.functions.register(domain_name, self.address, 1).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
