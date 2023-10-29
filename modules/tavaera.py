from typing import Union, Dict

from loguru import logger

from config import TAVAERA_CONTRACT, TAVAERA_ID_CONTRACT, TAVAERA_ABI, TAVAERA_ID_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Tavaera(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

    async def mint_id(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Tavaera ID")

        contract = self.get_contract(TAVAERA_ID_CONTRACT, TAVAERA_ID_ABI)
        
        tx_data = await self.get_tx_data(self.w3.to_wei(0.0003, "ether"))

        transaction = await contract.functions.mintCitizenId().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    async def mint_nft(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Tavaera NFT")

        contract = self.get_contract(TAVAERA_CONTRACT, TAVAERA_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.mint().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def mint(self, sleep_from: int, sleep_to: int):
        await self.mint_id()

        await sleep(sleep_from, sleep_to)

        await self.mint_nft()
