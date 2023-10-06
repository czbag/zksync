import time
from typing import Union

from loguru import logger
from web3 import Web3
from config import SAFE_ABI, SAFE_CONTRACT, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class GnosisSafe(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(SAFE_CONTRACT, SAFE_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    @retry
    @check_gas
    def create_safe(self):
        logger.info(f"[{self.account_id}][{self.address}] Create gnosis safe")

        setup_data = self.contract.encodeABI(
            fn_name="setup",
            args=[
                [self.address],
                1,
                ZERO_ADDRESS,
                "0x",
                Web3.to_checksum_address("0x2f870a80647BbC554F3a0EBD093f11B4d2a7492A"),
                ZERO_ADDRESS,
                0,
                ZERO_ADDRESS
            ]
        )

        transaction = self.contract.functions.createProxyWithNonce(
            Web3.to_checksum_address("0x1727c2c531cf966f902E5927b98490fDFb3b2b70"),
            setup_data,
            int(time.time()*1000)
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
