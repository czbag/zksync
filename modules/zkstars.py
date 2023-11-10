import random
from typing import Union

from loguru import logger
from config import ZKSTARS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class ZkStars(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

    @retry
    @check_gas
    async def mint(self, contracts: list, min_mint: int, max_mint: int, mint_all: bool, sleep_from: int, sleep_to: int):
        quantity_mint = random.randint(min_mint, max_mint)

        contracts = contracts if mint_all is True else random.sample(contracts, quantity_mint)

        logger.info(f"[{self.account_id}][{self.address}] Mint {quantity_mint} StarkStars NFT")

        for _, contract in enumerate(contracts, start=1):
            mint_contract = self.get_contract(self.w3.to_checksum_address(contract), ZKSTARS_ABI)

            mint_price = await mint_contract.functions.getPrice().call()
            nft_id = await mint_contract.functions.name().call()

            logger.info(f"[{self.account_id}][{self.address}] Mint #{nft_id} NFT")

            tx_data = await self.get_tx_data()
            tx_data.update({"value": mint_price})

            transaction = await mint_contract.functions.safeMint(
                self.w3.to_checksum_address("0x1C7FF320aE4327784B464eeD07714581643B36A7")
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())

            if _ != len(contracts):
                await sleep(sleep_from, sleep_to)
