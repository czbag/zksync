import random
from typing import Union

from loguru import logger
from config import ROCKETSAM_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class RocketSam(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

    async def get_deposit_amount(self, contract: str):
        contract = self.get_contract(self.w3.to_checksum_address(contract), ROCKETSAM_ABI)
        amount = await contract.functions.balances(self.address).call()
        return amount

    @retry
    @check_gas
    async def deposit(
            self,
            contracts: list,
            min_amount: float,
            max_amount: float,
            decimal: int,
            sleep_from: int,
            sleep_to: int,
            make_withdraw: bool,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(f"[{self.account_id}][{self.address}] Deposit to RocketSam")

        contract = self.get_contract(self.w3.to_checksum_address(random.choice(contracts)), ROCKETSAM_ABI)

        fee = await contract.functions.estimateProtocolFee(amount_wei).call()

        tx_data = await self.get_tx_data(amount_wei + fee)

        transaction = await contract.functions.depositWithReferrer(
            self.w3.to_checksum_address("0x1C7FF320aE4327784B464eeD07714581643B36A7"),
            amount_wei
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        if make_withdraw:
            await sleep(sleep_from, sleep_to)

            await self.withdraw([contract.address], sleep_from, sleep_to)

    @retry
    @check_gas
    async def withdraw(self, contracts: list, sleep_from: int, sleep_to: int):
        for _, contract in enumerate(contracts, start=1):
            amount = await self.get_deposit_amount(contract)

            if amount > 0:
                logger.info(
                    f"[{self.account_id}][{self.address}] Make withdraw from RocketSam | " +
                    f"{self.w3.from_wei(amount, 'ether')} ETH"
                )

                contract = self.get_contract(self.w3.to_checksum_address(contract), ROCKETSAM_ABI)

                tx_data = await self.get_tx_data()

                transaction = await contract.functions.withdraw().build_transaction(tx_data)

                signed_txn = await self.sign(transaction)

                txn_hash = await self.send_raw_transaction(signed_txn)

                await self.wait_until_tx_finished(txn_hash.hex())

                if _ != len(contracts):
                    await sleep(sleep_from, sleep_to)
            else:
                logger.error(f"[{self.account_id}][{self.address}] Deposit not found")
