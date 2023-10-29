import time
from typing import Union, Dict

from loguru import logger
from config import SAFE_ABI, SAFE_CONTRACT, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class GnosisSafe(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(SAFE_CONTRACT, SAFE_ABI)

    @retry
    @check_gas
    async def create_safe(self):
        logger.info(f"[{self.account_id}][{self.address}] Create gnosis safe")

        setup_data = self.contract.encodeABI(
            fn_name="setup",
            args=[
                [self.address],
                1,
                ZERO_ADDRESS,
                "0x",
                self.w3.to_checksum_address("0x2f870a80647BbC554F3a0EBD093f11B4d2a7492A"),
                ZERO_ADDRESS,
                0,
                ZERO_ADDRESS
            ]
        )

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.createProxyWithNonce(
            self.w3.to_checksum_address("0x1727c2c531cf966f902E5927b98490fDFb3b2b70"),
            setup_data,
            int(time.time()*1000)
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
